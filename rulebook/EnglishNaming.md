# Định danh code tiếng Anh: lý do, ca thật, cách đổi tên hàng loạt

> Tách nguyên văn khỏi `~/.claude/CLAUDE.md` §Code style cho nhẹ phần nạp mỗi lượt.
> Bản ngắn của luật ở `CLAUDE.md` §Code style; bản đầy đủ ở mục cuối tệp này.


## Quy trình đổi tên

**Khi đổi tên hàng loạt: 4 điều BẮT BUỘC** *(mỗi điều đổi bằng một lần hỏng thật)*:
1. 🔴 **Quét TOÀN REPO, liệt kê app TRƯỚC khi quét.** Chỉ quét app chính là sót.
2. 🔴 **`perl -pe` phải có `-Mutf8`**: thiếu nó thì `\b` khớp SAI giữa chữ có dấu: `s/\bVi\b/Wallet/` biến `"Việc cần làm"` thành `"Walletệc cần làm"`. Sau mỗi lượt thay phải quét `rg "(từ-mới)[à-ỹ]"`.
3. 🔴 **Tên NGẮN không thay được bằng regex toàn cục**: `\bra\b` khớp câu hiển thị *"đọc không ra"*, `\blap\b`/`\btao\b` khớp **route** `/lap-moi` `/job/tao`, `\bvi\b` khớp locale `'vi-VN'`. Cách chạy được: chỉ thay ở **dòng thuần code** (không chứa chữ có dấu), phần còn lại để type-checker chỉ mặt rồi **vá theo (dòng, CỘT)**.
4. 🔴 **So chuỗi hiển thị TRƯỚC/SAU**: trích mọi chuỗi có dấu ở `HEAD` và ở bản mới, bỏ phần `${…}`, rồi `comm`. Type-checker **mù hoàn toàn** với chuỗi; đây là cửa duy nhất.

**Đổi tên hàm/tham số SQL: type-checker KHÔNG bắt được:**
- Tên tham số RPC chỉ là **khoá object literal** ở client ⟹ đổi ở DB mà quên ở client thì **biên dịch sạch**, chỉ vỡ lúc chạy thật.
- ⟹ **Đối chiếu 2 chiều bằng máy**: trích `p_*` từ `create ... function` trong migration, trích `p_*` từ `.rpc('ten',{…})` ở client, rồi so.
- 📌 Nhận biết khi gọi thật: sai tên → `PGRST202` *(chữ của gateway)* · đúng tên → lỗi nghiệp vụ của chính hàm *(chữ của mình)*.
- ⚠️ Parse SQL phải **bỏ comment trước** rồi **đếm ngoặc**: `\(([^)]*)\)` dừng ở `)` đầu tiên, mà comment tham số hay có `(xem mục 2)` ⟹ cắt sớm, báo nhầm.

## Luật cốt lõi *(nguyên văn từ `CLAUDE.md`)*
### 🔴 MỌI ĐỊNH DANH CODE = TIẾNG ANH *(áp MỌI dự án)*
Bảng · cột · hàm SQL/RPC · **tên tham số RPC** · key JSON · biến · hàm TS · props React · hằng · component · **khoá StyleSheet** · **query param**: tất cả tiếng Anh.

🔴 Tiếng Việt CHỈ được ở **3 chỗ**: ① chuỗi hiển thị cho người dùng ② comment giải thích WHY ③ tên file/thư mục tài liệu `.md`.
📌 Ngoại lệ ③ chỉ cho tên **Plan, Idea, tài liệu** (`Plan_<ts>_<TenNgan>.md`); **khung** của flow hai vai đặt tiếng Anh: bộ luật `rulebook/` (`Roles.md`, `Details.md`, `EnglishNaming.md`), mục lục `Idea_*.md`, `Plan_*.md`, `11_DEBT/`, sổ `Active-Role.md`, script `activerole.py`.

⚠️ **Luật này áp cho code MỚI.** Dự án đang có tên tiếng Việt là **nợ cũ**: ⛔ **KHÔNG tự đại phẫu**, phải hỏi user và làm thành Plan riêng. Gặp tên cũ thì **đừng bắt chước**, viết mới bằng tiếng Anh; chỉ đổi những chỗ mình đang chạm.

🔴 **"Code MỚI" GỒM CẢ TỆP MỚI ĐẶT CẠNH TỆP CŨ.** Luật này **THẮNG** luật *"khớp style hiện có"* ở mục 3: thấy tệp bên cạnh đặt tên tiếng Việt thì **vẫn viết tiếng Anh**, ⛔ đừng bắt chước cho đồng bộ. 📌 *Dấu hiệu sắp sai:* đang đặt tên mới mà **nhìn sang tệp bên cạnh** để chọn ngôn ngữ. Nhìn vào LUẬT, ⛔ đừng nhìn hàng xóm.

🔴 **Ngoại lệ DUY NHẤT: khoá của kiểu/API ĐÃ tồn tại** *(thêm một phần tử vào mảng mà `type` đã khai `tenMien`, `daSong`)*, vì đổi là ⛔ không biên dịch được. Ngoại lệ chỉ phủ **khoá của kiểu cũ**, ⛔ KHÔNG phủ tên hằng, biến, hàm, component mới.
