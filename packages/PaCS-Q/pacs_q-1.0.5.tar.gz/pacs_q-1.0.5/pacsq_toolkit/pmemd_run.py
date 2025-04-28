import subprocess




def pmemd_run(crd, top, i, j):
    # 构建命令列表
    command = [
        'pmemd.cuda',
        '-O',
        '-i', '../../../md.in',
        '-o', 'md.out',
        '-ref', f'../../../{crd}',
        '-c', f'../../../{crd}',
        '-p', f'../../../{top}',
        '-r', f'md{i}_{j}.rst',
        '-x', f'md{i}_{j}.nc',
        '-v', 'mdvel'
    ]
    #print(command)


    # 打开 run.log 文件以写入标准错误
    with open('run.log', 'w') as stderr_file:
        try:
            result = subprocess.run(
                command,
                stderr=stderr_file,
                text=True
            )
            # 检查返回码
            result.check_returncode()
        except subprocess.CalledProcessError as e:
            print(f"Error，code：{e.returncode}")
            print("Please check 'run.log' for detail")
        except Exception as e:
            print(f"Error：{e}")
            print("Please check 'run.log' for detail")



def pmemd_run_cyc(crd, top, i, j, location, foldername, ref):
    # 构建命令列表
    command = [
        'pmemd.cuda',
        '-O',
        '-i', '../../../md.in',
        '-o', f'md{i}_{j}.out',
        '-ref', f'{location}/{foldername}/{i-1}/{ref}/min.rst',
        '-c', f'{location}/{foldername}/{i-1}/{ref}/min.rst',
        '-p', f'../../../{top}',
        '-r', f'md{i}_{j}.rst',
        '-x', f'md{i}_{j}.nc',
        '-v', 'mdvel'
    ]
    #print(command)


    # 打开 run.log 文件以写入标准错误
    with open('run.log', 'w') as stderr_file:
        try:
            result = subprocess.run(
                command,
                stderr=stderr_file,
                text=True
            )
            # 检查返回码
            result.check_returncode()
        except subprocess.CalledProcessError as e:
            print(f"Error，code：{e.returncode}")
            print("Please check 'run.log' for detail")
        except Exception as e:
            print(f"Error：{e}")
            print("Please check 'run.log' for detail")

