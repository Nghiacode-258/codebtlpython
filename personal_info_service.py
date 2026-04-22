import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate(r"D:\VS code\codewep\btlpython\key.json")
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()


def get_or_create_personal_info(firebase_uid, email="", full_name="", student_id="", phone=""):
    doc_ref = db.collection("personal_info").document(firebase_uid)
    doc = doc_ref.get()

    if doc.exists:
        return doc.to_dict()

    default_data = {
        "ma_sinh_vien": student_id or "",
        "ho_ten": full_name or "",
        "gioi_tinh": "",
        "ngay_sinh": "",
        "trang_thai_hoc": "Đang học",
        "cccd": "",
        "ngay_cap_cccd": "",
        "noi_cap_cccd": "",
        "so_dien_thoai": phone or "",
        "email_hoc_tap": email or "",
        "khoa_nganh": "",
        "chuyen_nganh": "",
        "quoc_tich": "Việt Nam",
        "dan_toc": "",
        "ton_giao": "",
        "tinh_thanh": "",
        "xa_phuong": "",
        "dia_chi_chi_tiet": "",
        "ngay_vao_dang_du_bi": "",
        "ngay_vao_dang_chinh_thuc": "",
        "so_bao_hiem": "",
        "ma_benh_vien": "",
        "ten_ngan_hang": "",
        "so_tai_khoan": "",
    }

    doc_ref.set(default_data)
    return default_data


def update_personal_info(firebase_uid, data: dict):
    db.collection("personal_info").document(firebase_uid).set(data, merge=True)