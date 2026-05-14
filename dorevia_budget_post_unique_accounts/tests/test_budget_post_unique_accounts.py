# -*- coding: utf-8 -*-

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestBudgetPostUniqueAccounts(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env.company
        cls.Post = cls.env["account.budget.post"]
        account_ids = set()
        for journal in cls.env["account.journal"].search(
            [("company_id", "=", cls.company.id)]
        ):
            acc = journal.default_account_id
            if acc:
                account_ids.add(acc.id)
        if len(account_ids) < 2:
            raise AssertionError(
                "Au moins deux comptes distincts (via journaux) sont requis pour les tests."
            )
        ids = list(account_ids)
        cls.acc_a = cls.env["account.account"].browse(ids[0])
        cls.acc_b = cls.env["account.account"].browse(ids[1])

    def test_same_account_on_two_active_posts_raises(self):
        p1 = self.Post.create(
            {
                "name": "Post A unique test",
                "company_id": self.company.id,
                "account_ids": [(6, 0, [self.acc_a.id])],
            }
        )
        with self.assertRaises(ValidationError):
            self.Post.create(
                {
                    "name": "Post B unique test",
                    "company_id": self.company.id,
                    "account_ids": [(6, 0, [self.acc_a.id])],
                }
            )
        p1.unlink()

    def test_after_archive_first_post_second_can_use_account(self):
        p1 = self.Post.create(
            {
                "name": "Post archive unique test",
                "company_id": self.company.id,
                "account_ids": [(6, 0, [self.acc_a.id])],
            }
        )
        p1.active = False
        p2 = self.Post.create(
            {
                "name": "Post after archive unique test",
                "company_id": self.company.id,
                "account_ids": [(6, 0, [self.acc_a.id])],
            }
        )
        self.assertTrue(p2.exists())
        (p1 | p2).unlink()

    def test_two_distinct_accounts_same_company_ok(self):
        p1 = self.Post.create(
            {
                "name": "Post distinct 1",
                "company_id": self.company.id,
                "account_ids": [(6, 0, [self.acc_a.id])],
            }
        )
        p2 = self.Post.create(
            {
                "name": "Post distinct 2",
                "company_id": self.company.id,
                "account_ids": [(6, 0, [self.acc_b.id])],
            }
        )
        self.assertTrue(p1.exists() and p2.exists())
        (p1 | p2).unlink()
