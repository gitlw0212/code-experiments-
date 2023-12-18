import logging
import os
import subprocess
import time


def run_command(cmd: str, work_path=os.getcwd(), timeout=None, print_log=False):
    p = subprocess.Popen(cmd, stderr=subprocess.STDOUT,
                         stdout=subprocess.PIPE, cwd=work_path, shell=True)
    t_beginning = int(time.time())
    logging.debug(f"running cmd: {cmd}")
    ret = ""
    while True:
        if p.poll() is not None:
            break
        for i in p.stdout:
            seconds_passed = int(time.time()) - t_beginning
            if timeout is not None and seconds_passed > timeout:
                p.kill()
                return "超时"
            if print_log:
                logging.info(i.decode('utf-8').strip())
            ret = ret + i.decode('utf-8')
    return ret


def run_shell(cmd, device_id, print_log=False):
    run_command(f'adb -s {device_id} shell \'{cmd}\'', print_log=print_log)


def rename_file(old_filename, new_filename, work_path):
    logging.info(f"rename file: {old_filename} -> {new_filename}, work_path: {work_path}")
    cmd = f'mv {old_filename} {new_filename}'
    run_command(cmd, work_path=work_path)


def get_ios_device_name(udid: str) -> str:
    cmd = 'bdc list-devices'
    ret = run_command(cmd)
    for line in ret.splitlines():
        if udid not in line:
            continue
        line = line.strip()
        return line.split('|')[6].strip()
    return 'unknown'


def get_model(device_os, device_id):
    if device_os == 'android':
        phone_name = run_command(
            f'adb -s {device_id} shell getprop ro.product.model').splitlines()[-1].strip()
        while 'adb: ' in phone_name or 'Otherwise' in phone_name:
            phone_name = run_command(
                f'adb -s {device_id} shell getprop ro.product.model').splitlines()[-1].strip()
            logging.info("通过adb检测model失败, 重试")
            time.sleep(3)
    else:
        phone_name = get_ios_device_name(device_id)

    return phone_name


def get_ios_ip(device_ip):
    cmd = f'bdc get-ip -u {device_ip}'
    ret = run_command(cmd).strip()
    return ret


def click_android(x, y, device_id):
    """
    点击手机坐标
    """
    ret = run_command(f'adb -s {device_id} shell wm size')
    r = ''
    for line in ret.splitlines():
        if 'Physical size:' in line:
            r = line
    size = r.split(':')[1].strip()
    size_x = int(size.split("x")[0])
    size_y = int(size.split("x")[1])
    click_x = size_x * x
    click_y = size_y * y
    run_command(f'adb -s {device_id} shell input tap {click_x} {click_y}')
    return


def click_android_real(click_x, click_y, device_id):
    run_command(f'adb -s {device_id} shell input tap {click_x} {click_y}')
    return


def click_ios(x, y, uid):
    cmd = f'bdc tap {x} {y} -u {uid}'
    run_command(cmd)
    return


def swip_ios(x1, y1, x2, y2, device_id, duration=1):
    cmd = f'bdc drag {x1} {y1} {x2} {y2} --duration {duration} -u {device_id}'
    logging.info(cmd)
    run_command(cmd)


def swip_android(x1, y1, x2, y2, device_id):
    """
    点击手机坐标
    """
    ret = run_command(f'adb -s {device_id} shell wm size')
    r = ''
    for line in ret.splitlines():
        if 'Physical size:' in line:
            r = line
    size = r.split(':')[1].strip()
    size_x = int(size.split("x")[0])
    size_y = int(size.split("x")[1])
    swip_x1 = size_x * x1
    swip_y1 = size_y * y1
    swip_x2 = size_x * x2
    swip_y2 = size_y * y2
    run_command(f'adb -s {device_id} shell input swipe  {swip_x1} {swip_y1} {swip_x2} {swip_y2}')
    return


def get_android_ip(device_id):
    cmd = f'adb -s {device_id} shell ip addr show wlan0|grep \"inet \"'
    ret = run_command(cmd)
    for item in ret.split():
        if '/' not in item:
            continue
        return item.split('/')[0].strip()


def kill_android_process(device_id, keyword):
    cmd = f"adb -s {device_id} shell ps -ef|grep {keyword}|grep -v grep|awk '" + "{print $2}" + \
          f"'|xargs adb -s {device_id} shell kill -9"
    run_command(cmd)


def kill_mac_process(keyword, signal=9):
    cmd = f'ps -ef|grep "{keyword}"|grep -v grep|awk ' + "'{print $2}'" + f'|xargs kill -{signal}'
    run_command(cmd)


if __name__ == '__main__':
    # print(get_android_ip("192.168.8.121:5555"))
# click_android(0.05, 0.08, 'a51dc11')
# click_ios(0.05, 0.1, '00008101-001538992278001E')
#     swip_ios(0.5, 0.8, 0.5, 0.1,'f2297c122175b9d94b343321719ddbc42be8c31a')
    click_ios(0.9,0.07,"00008110-001104CC0E86801E")
