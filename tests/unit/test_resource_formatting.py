from parliamentarian import (
    analyze_policy_string,
    is_arn_match,
    is_arn_strictly_valid,
    is_glob_match,
)
from parliamentarian.statement import is_valid_region, is_valid_account_id


class TestResourceFormatting:
    """Test class for resource formatting"""

    def test_resource_bad(self):
        policy = analyze_policy_string(
            """{
    "Version": "2012-10-17",
    "Statement": {
        "Effect": "Allow",
        "Action": "s3:listallmybuckets",
        "Resource": "s3"}}""",
            ignore_private_auditors=True,
        )
        assert len(policy.findings) == 1

    def test_resource_good(self):
        policy = analyze_policy_string(
            """{
    "Version": "2012-10-17",
    "Statement": {
        "Effect": "Allow",
        "Action": "s3:getobject",
        "Resource": "arn:aws:s3:::my_corporate_bucket/*"}}""",
            ignore_private_auditors=True,
        )
        print(policy.findings)
        assert len(policy.findings) == 0

    def test_is_valid_region(self):
        assert is_valid_region(""), "Empty regions are allowed"
        assert is_valid_region("us-east-1"), "This region is allowed"
        assert not is_valid_region("us-east-1f"), "This is an AZ, not a region"
        assert not is_valid_region("us-east-*"), "No regexes in regions"
        assert not is_valid_region("us"), "Not a valid region"
        assert not is_valid_region("us-east-1-f"), "Not a valid region"
        assert is_valid_region("us-gov-east-1"), "This is a valid govcloud region"

    def test_is_valid_account_id(self):
        assert is_valid_account_id(""), "Empty account id is allowed"
        assert is_valid_account_id("000000001234"), "This account id is allowed"
        assert not is_valid_account_id("abc"), "Account id must have 12 digits"
        assert not is_valid_account_id(
            "00000000123?"
        ), "Regex not allowed in account id"

    def test_arn_match(self):
        assert is_arn_match("object", "arn:*:s3:::*/*", "arn:*:s3:::*/*")
        assert is_arn_match("object", "*", "arn:*:s3:::*/*")
        assert is_arn_match("object", "arn:*:s3:::*/*", "*")
        assert is_arn_match("object", "arn:*:s3:::*/*", "arn:aws:s3:::*personalize*")
        assert is_arn_match("bucket", "arn:*:s3:::mybucket", "arn:*:s3:::mybucket")
        assert not is_arn_match(
            "bucket", "arn:*:s3:::mybucket", "arn:*:s3:::mybucket/*"
        ), "Bucket and object types should not match"
        assert not is_arn_match(
            "object", "arn:*:s3:::*/*", "arn:aws:s3:::examplebucket"
        ), "Object and bucket types should not match"
        assert is_arn_match("bucket", "arn:*:s3:::mybucket*", "arn:*:s3:::mybucket2")
        assert is_arn_match("bucket", "arn:*:s3:::*", "arn:*:s3:::mybucket2")
        assert not is_arn_match(
            "object", "arn:*:s3:::*/*", "arn:aws:logs:*:*:/aws/cloudfront/*"
        )
        assert not is_arn_match(
            "object", "arn:aws:s3:::*/*", "arn:aws:logs:*:*:/aws/cloudfront/*"
        )
        assert is_arn_match(
            "cloudfront",
            "arn:aws:logs:*:*:/aws/cloudfront/*",
            "arn:aws:logs:us-east-1:000000000000:/aws/cloudfront/test",
        )
        assert is_arn_match(
            "bucket",
            "arn:*:s3:::*",
            "arn:aws:s3:::bucket-for-client-${aws:PrincipalTag/Namespace}-*",
        )

    def test_is_arn_strictly_valid(self):
        assert is_arn_strictly_valid(
            "user",
            "arn:*:iam::*:user/*",
            "arn:aws:iam::123456789012:user/Development/product_1234/*",
        )

        assert is_arn_strictly_valid(
            "user", "arn:*:iam::*:user/*", "arn:aws:iam::123456789012:*"
        )

        assert is_arn_strictly_valid(
            "ssm",
            "arn:*:ssm::*:resource-data-sync/*",
            "arn:aws:ssm::123456789012:resource-data-sync/*",
        )

        assert not is_arn_strictly_valid(
            "ssm",
            "arn:*:ssm::*:resource-data-sync/*",
            "arn:aws:ssm::123456789012:resource-data-*/*",
        )

        assert not is_arn_strictly_valid(
            "user", "arn:*:iam::*:user/*", "arn:aws:iam::123456789012:*/*"
        )

        assert not is_arn_strictly_valid(
            "user", "arn:*:iam::*:user/*", "arn:aws:iam::123456789012:u*"
        )

        assert not is_arn_strictly_valid(
            "dbuser",
            "arn:*:redshift:*:*:dbuser:*/*",
            "arn:aws:redshift:us-west-2:123456789012:db*:the_cluster/the_user",
        )

    def test_arn_match_cloudtrail_emptysegments(self):
        assert not is_arn_match(
            "cloudtrail", "arn:*:cloudtrail:*:*:trail/*", "arn:::::trail/my-trail"
        )

    def test_arn_match_s3_withregion(self):
        assert not is_arn_match(
            "object", "arn:*:s3:::*/*", "arn:aws:s3:us-east-1::bucket1/*"
        )

    def test_arn_match_s3_withaccount(self):
        assert not is_arn_match(
            "object", "arn:*:s3:::*/*", "arn:aws:s3::123412341234:bucket1/*"
        )

    def test_arn_match_s3_withregion_account(self):
        assert not is_arn_match(
            "object", "arn:*:s3:::*/*", "arn:aws:s3:us-east-1:123412341234:bucket1/*"
        )

    def test_arn_match_iam_emptysegments(self):
        assert not is_arn_match(
            "role", "arn:*:iam::*:role/*", "arn:aws:iam:::role/my-role"
        )

    def test_arn_match_iam_withregion(self):
        assert not is_arn_match(
            "role", "arn:*:iam::*:role/*", "arn:aws:iam:us-east-1::role/my-role"
        )

    def test_arn_match_apigw_emptysegments(self):
        assert not is_arn_match(
            "apigateway",
            "arn:*:apigateway:*::*",
            "arn:aws:apigateway:::/restapis/a123456789/*",
        )

    def test_arn_match_apigw_withaccount(self):
        assert not is_arn_match(
            "apigateway",
            "arn:*:apigateway:*::*",
            "arn:aws:apigateway:us-east-1:123412341234:/restapis/a123456789/*",
        )

    def test_is_glob_match(self):
        tests = [
            # string1, string2, whether they match
            ("a", "b", False),
            ("a", "a", True),
            ("a", "*", True),
            ("*", "a", True),
            ("a*a", "*", True),
            ("a*a", "a*b", False),
            ("a*a", "aa", True),
            ("a*a", "aba", True),
            ("*a*", "*b*", True),  # Example "ab"
            ("a*a*", "a*b*", True),  # Example "aba"
            ("aaaaaa:/b", "aa*a:/b", True),
            ("*/*", "*personalize*", True),  # Example "personalize/"
            ("", "*", True),
            ("", "**", True),
            ("", "a", False),
            ("**", "a", True),
        ]

        for s1, s2, expected in tests:
            assert (
                is_glob_match(s1, s2) == expected
            ), "Matching {} with {} should return {}".format(s1, s2, expected)
