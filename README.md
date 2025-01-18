# SocietyPasswordDict
社工字典生成

## 功能介绍
本工具用于生成基于个人信息的密码字典，通过组合个人信息、数字和特殊字符生成可能的密码组合。这可以帮助用户在进行社会工程学攻击时，生成针对性的密码字典，提高攻击成功率。

## 使用方法
1. 将个人信息保存在文本文件中，每行一条信息。例如，个人信息文件（info.txt）可以包含以下信息：
~~~text
姓名全拼:chanzixuan
姓名简拼:czx
手机号码:19071966450
生日:20101003
社交帐号:45484895
身份证号:650101198406021987
有意义的字符或数字:807512
子女生日:20450404
子女手机号:17711907865
微博账号id:54546896
微博账号密码:45484895@czx
~~~
2. 运行程序，通过命令行参数指定个人信息文件、生成的字典文件和密码长度。例如：
~~~bash 
python dictsociety.py --dict_file output.txt --info_file myinfo.txt --password_length 6
~~~
## 参数说明
- `--dict_file`: 生成的密码字典文件路径，默认为 `dict.txt`。这是程序生成的密码组合将要保存的文件。
- `--info_file`: 个人信息文件路径，默认为 `info.txt`。这是包含个人信息的文件，程序将使用这些信息生成密码组合。
- `--password_length`: 密码长度，默认为 `4`。这是生成密码组合时指定的密码长度。

## 示例
~~~bash
 python dictsociety.py --dict_file output.txt --info_file myinfo.txt --password_length 6
~~~