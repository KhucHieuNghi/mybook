# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions

class Sach(models.Model):
    # translate: dich model này sang ngôn ngữ khác trong CSDL
    # auto: Tự động tạo bảng CSDL
    # table: thay đổi tên mặc định của _name
    # depends: Khai báo những trường phụ thuộc vào model này, để thực hiện các câu truy vấn, dùng cho báo cáo
    _name = "quanlysach.book"
    _rec_name = "ten_sach"
    _auto = True
    _table="mybook"
    _description=u"Sách của tui"
    _order="tacgia_chinh, ten_sach"
    _translate = False


    ten_sach = fields.Char("Tên sách", size= 50, translate=True, default="Sách mới")
    ma_sach = fields.Char("Mã sách")
    mote = fields.Text("Mô tả", help="Viết mô tả ở đây")
    loaisach = fields.Selection(string ="Loại sách",
                                selection=[("moi", "Mới"),
                                           ("cu", "Cũ")])
    ngay = fields.Date("Ngày xuất bản", required=True)

    ngay_ban = fields.Date("Ngày bán")
    thoi_gian = fields.Datetime("Thời gian", index=True)
    type_bool = fields.Boolean(string = "Để cho vui", readonly=True)
    anh_bia = fields.Binary(string="Ảnh bìa")
    html = fields.Html("Văn bản")
    soluong = fields.Integer("Số lượng")
    giagoc = fields.Float("Giá gốc")
    giatri = fields.Float("Giá bán", compute="_tinh_giab", store=True)
    trangthai = fields.Selection(string ="Trạng thái",
                                 selection = [('con', "Còn sách"),
                                              ('het', "Hết sách"),
                                              ('shet', "Sắp hết sách")])
    tacgia_chinh = fields.Many2one(
        comodel_name="quanlysach.tacgia",
        string="Tác giả chính"
    )
    tacgia_phu = fields.Many2many(
        comodel_name="quanlysach.tacgia",
        string="Tác giả phụ"
    )

    _sql_constraints = [('ten_sach_la_duy_nhat','UNIQUE(ten_sach)',u'Tên trùng rồi chọn cái khác đi')]
    _depends={}

    @api.multi
    @api.constrains("ten_sach")
    def _kiem_tra_ten_sach(self):
        for rec in self:
            if len(rec.ten_sach) < 6:
                raise exceptions.ValidationError("Tên sách ngắn đặt lại đi lớn hơn 6 ký tự nha")

    @api.onchange("tacgia_chinh")
    def _them_tg_ten_sach(self):
        pos = self.ten_sach.rfind("-")
        if int(pos) == -1:
            self.ten_sach += " - " + self.tacgia_chinh.name
        else:
            self.ten_sach = self.ten_sach[0:pos + 2] + self.tacgia_chinh.name

    @api.depends("soluong", "giagoc")
    def _tinh_giab(self):
        for rec in self:
            if rec.soluong > 100:
                rec.giatri = rec.giagoc *1.2
            elif 50 < rec.soluong <= 100:
                rec.giatri = rec.giagoc * 1.5
            else:
                rec.giatri = rec.giagoc * 2.0
    # Phương thức hỗ trợ
    @api.model
    def doi_trang_thai(self, sl):
        if 0 < sl < 10:
            self.trangthai = "shet"
        elif sl == 0:
            self.trangthai = "het"
        else:
            self.trangthai = "con"

    @api.onchange("soluong")
    def thaydoi_soluong(self):
        self.doi_trang_thai(self.soluong)