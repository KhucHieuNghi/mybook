# -*- coding: utf-8 -*-

from odoo import models, fields

class TacGia(models.Model):
    _name = "quanlysach.tacgia"
    # _rec_name = "ten_sach"
    name = fields.Char("Tên tác giả")
    ngaysinh = fields.Date("Ngày sinh")

    sach_tacgia = fields.One2many(
        comodel_name="quanlysach.book",
        inverse_name="tacgia_chinh",
        string="Sách của tác giả"
    )


