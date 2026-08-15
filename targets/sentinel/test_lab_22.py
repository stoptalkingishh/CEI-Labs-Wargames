import unittest
from email import policy
from email.parser import Parser
from email.utils import parseaddr

import answer_service
import runtime


class Lab22RuntimeTests(unittest.TestCase):
    def test_static_message_evidence_supports_the_exact_answer(self):
        message = Parser(policy=policy.default).parsestr(runtime.LAB_22_MESSAGE)

        self.assertEqual(message["From"].addresses[0].domain, runtime.ANSWERS["sentinel-22"]["from_domain"])
        self.assertEqual(parseaddr(str(message["Return-Path"]))[1].rsplit("@", 1)[1], runtime.ANSWERS["sentinel-22"]["return_path_domain"])
        self.assertIn("spf=pass smtp.mailfrom=invoice-notice.example", message["Authentication-Results"])
        self.assertIn("dmarc=fail header.from=northstar.training", message["Authentication-Results"])
        self.assertIn("192.0.2.44", message["Received"])
        self.assertIn("Static synthetic RFC-822 training fixture", message.get_content())

    def test_submission_requires_the_lab_22_account_and_exact_tuple(self):
        answer = runtime.ANSWERS["sentinel-22"]
        credentials = {"sentinel-22": "team-secret"}
        submission = {"lab": "sentinel-22", "answer": answer}

        self.assertEqual(answer_service.release(submission, "sentinel22", runtime.ANSWERS, credentials), "team-secret")
        with self.assertRaises(SystemExit):
            answer_service.release(submission, "sentinel23", runtime.ANSWERS, credentials)
        with self.assertRaises(SystemExit):
            answer_service.release(
                {"lab": "sentinel-22", "answer": {**answer, "dmarc": "pass"}},
                "sentinel22",
                runtime.ANSWERS,
                credentials,
            )
        with self.assertRaises(SystemExit):
            answer_service.release(
                {"lab": "sentinel-22", "answer": {**answer, "extra": "field"}},
                "sentinel22",
                runtime.ANSWERS,
                credentials,
            )


if __name__ == "__main__":
    unittest.main()
