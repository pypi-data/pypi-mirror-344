import subprocess




def sander_run_mpi(crd, top, i, j):
    # 构建命令列表
    command = [
        'mpirun', '-np', '24',
        'sander.MPI',
        '-O',
        '-i', '../../../qmmm.in',
        '-o', 'qmmm.out',
        '-ref', f'../../../{crd}',
        '-c', f'../../../{crd}',
        '-p', f'../../../{top}',
        '-r', f'qmmm{i}_{j}.rst',
        '-x', f'qmmm{i}_{j}.nc'
    ]


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



def sander_run_mpi_cyc(crd, top, i, j, location, foldername, ref):
    # 构建命令列表
    command = [
        'mpirun', '-np', '24',
        'sander.MPI',
        '-O',
        '-i', '../../../qmmm.in',
        '-o', f'qmmm{i}_{j}.out',
        '-ref', f'{location}/{foldername}/{i-1}/{ref}/min.rst',
        '-c', f'{location}/{foldername}/{i-1}/{ref}/min.rst',
        '-p', f'../../../{top}',
        '-r', f'qmmm{i}_{j}.rst',
        '-x', f'qmmm{i}_{j}.nc'
    ]


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

#sander_run_mpi_cyc("test", "test", 1, 3, "/usr/location", "MDrun", 3)
