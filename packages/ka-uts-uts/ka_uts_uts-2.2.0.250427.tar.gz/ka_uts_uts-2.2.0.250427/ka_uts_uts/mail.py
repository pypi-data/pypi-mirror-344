from typing import Any

from ka_uts_log.log import LogEq
from ka_uts_uts.utils.pac import Pac
from ka_uts_uts.ioc.yaml_ import Yaml_

from ka_uts_uts.mailrcv import MailRcv
from ka_uts_uts.mailsnd import MailSnd

from email.mime.text import MIMEText

TyDic = dict[Any, Any]
TnAny = None | Any


class Mail:

    @staticmethod
    def snd(kwargs: TyDic) -> None:
        _package = kwargs.get('package', '')
        _in_path_aod_send = kwargs.get('in_path_aod_send', '')
        print(f"Email.send _package = {_package}")
        print(f"Email.send _in_path_aod_send = {_in_path_aod_send}")
        _path = Pac.sh_path_by_package(_package, _in_path_aod_send)
        print(f"Email.send _path = {_path}")
        _aod_send: TnAny = Yaml_.read_with_safeloader(_path)
        if not _aod_send:
            raise Exception(f"Content of yaml file = {_path} is undefined or empty")
        print(f"Email.send _aod_send = {_aod_send}")

        for _d_send in _aod_send:
            LogEq.debug("_d_send", _d_send)
            _msg = MailSnd.create(_d_send)
            _aod_path = _d_send.get('attachements')
            LogEq.debug("_aod_path", _aod_path)
            if _aod_path:
                _body = _d_send.get('body')
                _msg.attach(MIMEText(_body, 'plain'))
                MailSnd.add_attachements(_msg, _aod_path, kwargs)

            # Send the email
            MailSnd.send(_msg, _d_send)

    @staticmethod
    def rcv(kwargs: TyDic) -> None:
        # Connect to the server
        _sw_ssl = kwargs.get('sw_ssl', True)
        _host = kwargs.get('host')
        _mail = MailRcv.connect(_sw_ssl, _host)
        # Login to your account
        MailRcv.login(_mail, kwargs)

        # Select the mailbox you want to check
        _mail.select("inbox")
        # Search for all emails in the inbox
        # status, messages = _mail.search(None, "ALL")
        # Search for unread emails
        status, messages = _mail.search(None, 'UNSEEN')
        # Convert messages to a list of email IDs

        # Reading Emails
        # Now that you have the email IDs, you can fetch and read the emails.
        # Here’s how to do it:
        # Fetch the latest email
        # latest_email_id = _email_ids[-1]
        MailRcv.yield_body(_mail, messages[0])

        # Logout
        _mail.logout()
