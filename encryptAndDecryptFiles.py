# 使用aes加解密当前文件夹里的文件

# 导入模块
import os
import pyAesCrypt

def jiami():
    # 设置密码和缓冲区大小
    password = input("输入256位加密密码")
    bufferSize = 64 * 1024

    # 获取当前文件夹下的所有文件名
    files = os.listdir()

    # 创建子文件夹"decrypt"，如果不存在的话
    if "decrypt" not in files:
        os.mkdir("decrypt")

    # 遍历所有文件，加密并保存到子文件夹"decrypt"
    for file in files:
        # 跳过子文件夹"decrypt"和本程序文件
        if file == "decrypt" or file.endswith(".py"):
            continue
        # 生成加密后的文件名，添加".aes"后缀
        encryptedFile = file + ".aes"
        # 加密文件，并保存到子文件夹"decrypt"
        pyAesCrypt.encryptFile(file, "decrypt/" + encryptedFile, password, bufferSize)

    print('加密完成')

def jiemi():

    # 设置密码和缓冲区大小
    password = input("输入解密密码")
    bufferSize = 64 * 1024

    # 获取子文件夹"decrypt"下的所有文件名
    files = os.listdir("decrypt")

    # 遍历所有文件，解密并保存到当前文件夹
    for file in files:
        # 生成解密后的文件名，去掉".aes"后缀
        decryptedFile = file[:-4]
        # 解密文件，并保存到当前文件夹
        pyAesCrypt.decryptFile("decrypt/" + file, decryptedFile, password, bufferSize)

    print("解密完成")

choice = input("请输入数字,加密:1,解密：2")

print(choice)

if choice == "1":
    jiami()
elif choice =="2":
    jiemi()
else:
    print("请输入正确数字，程序即将退出...")
