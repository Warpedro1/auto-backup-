import shutil
import os
from datetime import datetime
import time

def backup(org, dest):
    if not os.path.exists(org):
        print(f"Source directory doesnt exist: {org} ")
    
    if not os.path.exists(dest):
        print(f"Destination directory doesnt exist: {dest} ")
    
    for file_name in os.listdir(org):
        file_path = os.path.join(org, file_name)

        if os.path.isfile(file_path):
            try:
                shutil.copy2(file_path, dest)
                print(f"{file_name} file was back up to {dest} ")
            except shutil.Error as e:
                print(f"ERROR while tryting to bakc up files from {org} to {dest} /n {e}")

def backups_log(org, fromLog, toLog):
    try:
        current_time = time.time()
        current_time_str = datetime.fromtimestamp(current_time).strftime('%Y-%m-%d %H:%M:%S')

        with open(toLog, 'a') as toFile:
            toFile.write(f"---------------------------------------------- log {current_time_str}---------------------------------------------\n")
        with open(fromLog, 'a') as fromFile:
            fromFile.write(f"---------------------------------------------- log {current_time_str}---------------------------------------------\n")

        for file_name in os.listdir(org):
            file_path = os.path.join(org, file_name)

            if os.path.isfile(file_path):
                file_size = os.path.getsize(file_path)
                creation_time = os.path.getctime(file_path)
                mod_time = os.path.getmtime(file_path)

                creation_time_str = datetime.fromtimestamp(creation_time).strftime('%Y-%m-%d %H:%M:%S')
                mod_time_str = datetime.fromtimestamp(mod_time).strftime('%Y-%m-%d %H:%M:%S')

                try:
                    with open(fromLog, 'a') as fromFile:
                        fromFile.write(f"nome: {file_name}, tamanho: {file_size}, dataCriacao: {creation_time_str}, dataUltimaMod: {mod_time_str}\n")
                        print(f"{file_name} metadata was logged to {fromLog}")
                except EOFError as e:
                    print(f"Error {e} while writing {file_name} in {fromLog}")      

                if (current_time - creation_time) <= 72 * 3600: 
                    try:
                        with open(toLog, 'a') as toFile:
                            toFile.write(f"nome: {file_name}, tamanho: {file_size}, dataCriacao: {creation_time_str}, dataUltimaMod: {mod_time_str}\n")
                            print(f"{file_name} metadata was logged to {toLog}")
                    except EOFError as e:
                        print(f"Error {e} while writing {file_name} in {toLog}")
                else:
                    remove_file(file_path)
                           
    except OSError as e:
            print(f"Error accessing file {file_path}: {e}")



def remove_file(file_path):
    try:
        os.remove(file_path)
        print(f"SUCCESSFULY removed {file_path}")
    except Exception as e:
        print(f"FAIL to remove {file_path}")

if __name__ == "__main__":
    
    org = r"C:\Users\warpe\Documents\Cesar\7\Aws\valcann\problema1\home\valcann\backupsFrom"
    dest = r"C:\Users\warpe\Documents\Cesar\7\Aws\valcann\problema1\home\valcann\backupsTo"
    fromLog = r"C:\Users\warpe\Documents\Cesar\7\Aws\valcann\problema1\home\valcann\backupsFrom.log"
    toLog = r"C:\Users\warpe\Documents\Cesar\7\Aws\valcann\problema1\home\valcann\backupsTo.log"

    backups_log(org, fromLog, toLog)
    backup(org,dest)
    