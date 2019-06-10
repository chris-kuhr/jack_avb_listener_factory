$(document).ready(function(){

    function showDetails( endpointType ){
        $('#'+endpointType.EPType+'_ep_name').text( endpointType.EPName );
        
        // bg color white as default
        // red if jack client has failed, 
        // yellow if started, 
        // green if active
        $('#'+endpointType.EPType+'_jack_client_name').text( endpointType.JACKName );
        
        
        $('#'+endpointType.EPType+'_MACaddr').text( endpointType.MACaddr );
        $('#'+endpointType.EPType+'_SID').text( endpointType.SID );
        $('#'+endpointType.EPType+'_dst_stream_MACaddr').text( endpointType.DSTMAC );
        $('#'+endpointType.EPType+'_channel_count').text( endpointType.CCnt );
    }





    var ws = new WebSocket("ws://localhost:5678/");
    
        
        
    ws.onmessage = function ( event ) {
        json_obj = $.parseJSON( event.data );        
	    console.log(json_obj)
	    
	    if( json_obj.discovered  ){  // new entity showed up
	        for (var key in json_obj.discovered){
	            var eptype = json_obj.discovered[key]
	            showDetails( eptype );
	            
	            if(eptype.EPType == "talker") {
        	        $('#matrix tr:eq(0) td:eq('+eptype.IDX+')').text( eptype.EPName );
	            } 
	            if(eptype.EPType == "listener") {
	                $('#matrix tr:eq('+eptype.IDX+') td:eq(0)').text( eptype.EPName );
	            }
	        }
	    }
	    
	    
	    if( json_obj.respListener ){
            showDetails( json_obj.respListener[0] );            
	        $('#matrix tr:eq('+json_obj.respListener[0].IDX+') td:eq(0)').text( json_obj.respListener[0].EPName );
		} 
	    
	    if( json_obj.respTalker ){
            showDetails( json_obj.respTalker[0] );            
	        $('#matrix tr:eq(0) td:eq('+json_obj.respTalker[0].IDX+')').text( json_obj.respTalker[0].EPName );
	    } 
	    
	    if( json_obj.connected  ){  // show status of connection
	        var rowIdx = 0;
	        var colIdx = 0;
	        var bgColor = "#FFFFFF";
	        
	        for (var key in json_obj.connected){
    	        console.log(key, json_obj.connected[key]);
    	        if( json_obj.connected[key].status ) {
	                if( json_obj.connected[key].status == "OK"){
        	            console.log("ok", json_obj.connected[key].status);
               	        bgColor = "#00FF00";
                    } else {
                        console.log("not ok", json_obj.connected[key].status);
                        bgColor = "#FF0000";
                    } 
                } else {
	                var eptype = json_obj.connected[key];
                    showDetails( eptype );
                    
                    if(eptype.EPType == "talker") {
                        colIdx = eptype.IDX;
                    } 
                    if(eptype.EPType == "listener") {
                        rowIdx = eptype.IDX;
                    }
                }
	        }
	        console.log(rowIdx,colIdx);
            $('#matrix tr:eq('+rowIdx+') td:eq('+colIdx+')').css("background-color", bgColor); 
	    }
	    
    };//onmessage
            
    
    
    
    
    // cross matrix logic
    $('#matrix tr td').click(function() {
		var colIdx = $(this).closest('td').index();
        var rowIdx = $(this).closest('tr').index();   
		
		if(rowIdx == 0 && colIdx == 0){
		    alert("quitting");
            ws.send({"Quit":True});
		}		
		else if(rowIdx == 0 ||  colIdx == 0 && (rowIdx != colIdx) ){   		
    		if(colIdx == 0){   		    
                ws.send(JSON.stringify({"reqListener":rowIdx}));
            } else if (rowIdx == 0){
                ws.send(JSON.stringify({"reqTalker":colIdx}));
            }     		
		} else if(rowIdx > 0 ||  colIdx > 0){		
		    var listenerName = $('td:first', $(this).parents('tr')).text()
		    var talkerName = $('#matrix').find('td').eq( colIdx ).text();		    
		    var comStr = "listener "+listenerName+" Id: "+colIdx+" from talker "+talkerName+" Id: "+rowIdx
		    
	        if( $(this).text() != "x" ){ // Connect
	            $(this).text("x"); 
	            var logStr =  "Connect " + comStr
	            alert(logStr);
	            ws.send(JSON.stringify({"connect":[{"listener":listenerName,"talker":talkerName}]}));      
	        } else { //Disconnect
	            $(this).text("o");
	            var logStr = "Disconnect " + comStr
	            alert(logStr);
	            ws.send(JSON.stringify({"disconnect":[{"listener":listenerName,"talker":talkerName}]}));     
    		}
		} else {
    		console.log(rowIdx, colIdx);		
		}
		
		
		
    }); // click
    
    
});// ready()


