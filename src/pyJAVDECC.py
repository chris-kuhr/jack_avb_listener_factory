import mmap
import os
import sys
import time
import posix_ipc

import ipc_utils as utils
from avdeccEntity import AVDECCEntity, serializeList2Str, deserializeStr2List

if __name__ == '__main__':

    params = utils.read_params()
    # Create the shared memory and the semaphore.
    memory = posix_ipc.SharedMemory(params["SHARED_MEMORY_NAME"], posix_ipc.O_CREX, size=params["SHM_SIZE"])
    semaphore = posix_ipc.Semaphore(params["SEMAPHORE_NAME"], posix_ipc.O_CREX)

    # MMap the shared memory
    mapfile = mmap.mmap(memory.fd, memory.size)

    semaphore.release()

    while(True):
        
        semaphore.acquire()
        serStr = utils.read_from_memory(mapfile)
        semaphore.release()

        serList = deserializeStr2List(serStr)

        entity_list2 = []
        for device in serList:    
            dummy = AVDECCEntity()  
            if dummy.decodeString(device) > 0:
                entity_list2.append(dummy)
                print(dummy.encodeString())
            else:
                break

        time.sleep(1)
    # I could call memory.unlink() here but in order to demonstrate
    # unlinking at the module level I'll do it that way.
    posix_ipc.unlink_shared_memory(params["SHARED_MEMORY_NAME"])

    semaphore.release()

    # I could also unlink the semaphore by calling
    # posix_ipc.unlink_semaphore() but I'll do it this way instead.
    semaphore.unlink()
    mapfile.close()
