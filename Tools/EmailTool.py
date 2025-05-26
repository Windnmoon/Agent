import webbrowser
import urllib.parse
import re


def _is_valid_email(email: str) -> bool:
    receivers = email.split(';')
    # 正则表达式匹配电子邮件
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    for receiver in receivers:
        if not bool(re.match(pattern, receiver.strip())):
            return False
    return True


def send_email(
        to: str,
        subject: str,
        body: str,
        cc: str = None, # cc（抄送）：用于指定邮件的抄送收件人，抄送收件人的邮箱地址对主要收件人和抄送收件人可见。
        bcc: str = None, # bcc（密件抄送）：用于指定邮件的密件抄送收件人，密件抄送收件人的邮箱地址对主要收件人和抄送收件人不可见。
) -> str:
    """给指定的邮箱发送邮件"""

    if not _is_valid_email(to):
        return f"电子邮件地址 {to} 不合法"

    # 对邮件的主题和正文进行URL编码
    subject_code = urllib.parse.quote(subject)
    body_code = urllib.parse.quote(body)
    # 对邮件主题和正文进行 URL 编码，可以确保 mailto 链接的正确性和可靠性。urllib.parse.quote 函数将特殊字符转换为百分号编码，使得这些字符能够在 URL 中安全传输，并被邮件客户端正确解析和显示。
    # subject_code所在行代码对邮件主题 subject 进行 URL 编码，并将结果存储在 subject_code 变量中。例如，如果 subject 是 "你好，世界！"，编码后的结果可能是 "%E4%BD%A0%E5%A5%BD%EF%BC%8C%E4%B8%96%E7%95%8C%EF%BC%81"。

    # 构造mailto链接
    mailto_url = f'mailto:{to}?subject={subject_code}&body={body_code}'
    if cc is not None:
        cc = urllib.parse.quote(cc)
        mailto_url += f'&cc={cc}'
    if bcc is not None:
        bcc = urllib.parse.quote(bcc)
        mailto_url += f'&bcc={bcc}'

    webbrowser.open(mailto_url)

    return f"状态: 成功\n备注: 已发送邮件给 {to}, 标题: {subject}"
