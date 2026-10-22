---
name: reviewplan
description: Rà NỘI DUNG một Plan (hoặc Idea, chế độ hai lớp) vừa viết xong (khác checkplan vốn rà TRẠNG THÁI) - soi 4 lớp (logic · đọc toàn bộ bắt mâu thuẫn · ĐO LẠI từng con số · kiểm quy ước), lặp tới khi PASS, tự sửa lỗi hình thức và số liệu nhưng HỎI khi đụng phạm vi hoặc cách làm. Dùng khi user nói "reviewplan", "review plan", "soi plan", "soát plan", "kiểm plan vừa viết", "plan này có ổn không", hoặc ngay sau khi lập xong một Plan. ⚠️ Cụm "rà plan" và "kiểm tra plan" thuộc về checkplan (rà TRẠNG THÁI); nghe hai cụm đó mà ngữ cảnh là Plan vừa viết xong thì HỎI user muốn skill nào.
---

# ReviewPlan: soi Plan trước khi code

Viết mọi văn bản bằng **tiếng Việt**. Rà **nội dung** Plan: đúng chưa, đủ chưa, có tự mâu thuẫn không.
⚠️ **KHÁC `checkplan`**: `checkplan` rà *trạng thái* (xong chưa). Skill này chạy **ngay sau khi viết xong Plan**, trước khi code.

> **Bài học cốt lõi (lý do skill tồn tại):** một phiên rà một bộ Plan **10 vòng**, bắt **hơn 40 chỗ sai**. Vòng đầu tưởng sạch, **vòng 3 vẫn ra 18 lỗi**, **vòng 6 còn ra một con số sai gần 7 lần**. Nặng nhất: một bước **tự phá mục tiêu của chính Plan** mà mọi cửa kiểm vẫn báo xanh, và một câu **rơi mất chữ "KHÔNG"** biến lời cảnh báo thành lời cho phép.

## Bước 0. Xác định phạm vi
- Cây ở **gốc workspace** (mọi dự án cùng khuôn): tệp nằm yên trong `05_PLANS/Plan_List/`, `01_IDEA/Idea_List/`; trạng thái là dòng mục lục
  `05_PLANS/Plan_Draft.md` *(Plan chờ rà)*, `01_IDEA/Idea_Draft.md` *(chế độ Idea)*. User ⛔ không nêu tên thì đọc mục lục đó để chọn, chỉ dòng **Đang cầm** trống;
  nhận rà thì `${CLAUDE_PLUGIN_ROOT}/scripts/activerole.py index hold <tc> <mã>` trước, đọc mã ở **dòng 1**: phải là `DA_CAM`; `DA_CO_NGUOI_CAM` thì chọn dòng khác;
  `NHIEU_DONG` thì gọi lại bằng đường ở dòng `DONG`; mã lỗi khác thì DỪNG, báo user.
  Tệp nằm trong `01_IDEA/Idea_List/` ⟹ **chế độ Idea** (mục cuối; xét theo vị trí, ⛔ không theo tiền tố tên).
- 🔴 Gốc ⛔ không có mục lục thì ⛔ ĐỪNG ĐOÁN: bám `CLAUDE.md`, không thấy thì **HỎI user**.
- **Rà cả Idea đi kèm** (link ở đầu Plan): phiên ấy có 3 lỗi nằm đúng chỗ Idea lệch với Plan.
- ⚠️ **Cạm bẫy cwd:** Bash tool hay reset về gốc workspace → dùng đường tuyệt đối hoặc `(cd <thư-mục> && …)`, ⛔ không `cd` trần.
- 🔴 **`zsh` KHÔNG tách biến thành danh sách tệp:** `grep ... $F` với `F="a b c"` coi cả chuỗi là MỘT tên tệp ⟹ phép quét **chạy mà không đọc gì**. Liệt kê đường dẫn tường minh.

## Bốn lớp rà (không lớp nào thay được lớp nào)

**Lớp 1 · LOGIC.** Mỗi khẳng định kỹ thuật hỏi *"đã đo chưa, hay đang đoán?"*. Bắt: cách làm bất khả thi, bước thiếu, tính năng đang chạy bị bỏ sót khỏi đặc tả. ⚠️ Mù với mâu thuẫn giữa các mục.

**Lớp 2 · ĐỌC TOÀN BỘ, không chỉ chỗ vừa sửa.** Đọc từ dòng đầu tới dòng cuối (dùng `sed -n` theo lát, ⛔ không `cat` một lần). Bắt: mục 1 chỏi mục 7, một bước vừa bảo sửa tệp vừa bảo gỡ nó, tham chiếu trỏ mục đã đổi nội dung, **chữ rơi mất làm đảo nghĩa**. 🔴 Lớp này bắt 18/40 lỗi của phiên ấy.

🔴 **HUB ghi "🩹 đã vá" ⛔ KHÔNG chứng minh FILE CON đã vá.** Master của module viết *"đã sửa mâu thuẫn: P1 §5 khai P3 độc lập, bản này chốt P3 phụ thuộc P2"*, mở `P1 §5` ra thì câu cũ **còn nguyên si**. Ba chỗ dính cùng kiểu trong một module: lượt vá trước bác một tiền đề ở phần THÂN, nhưng **bảng câu hỏi chốt và bảng rủi ro vẫn mang nguyên tiền đề đã bị bác** ⟹ người thi công đọc bảng ấy là chép lại đúng cái sai.
📌 **Cách bắt: sau khi bác một tiền đề, `grep` chính chuỗi vừa bác trên TOÀN MODULE**, ⛔ đừng chỉ sửa chỗ đang gõ.

**Lớp 3 · ĐO LẠI TỪNG CON SỐ.** Trích mọi số trong Plan rồi đo bằng máy: **hỏi thẳng DB**, `curl` trang thật. 🔴 Vì sao bắt buộc: một con số **sai đều từ đầu ở mọi tệp** thì ⛔ không mâu thuẫn với gì cả, đọc bao nhiêu lần cũng không thấy, **chỉ lộ khi đo**.
🔑 **Góc đo mạnh nhất: KIỂM TỪNG CON SỐ BẰNG CODE THẬT (`grep` và ĐẾM)**, khác hẳn góc "đọc và đối chiếu nội bộ" của lớp 2.
⚠️ **Hai số đá nhau CÓ THỂ cùng đúng, đếm thật trước khi gọi là lỗi.** `46` với `48` trông như mâu thuẫn, hoá ra **đo hai thứ khác nhau** *(48 chỗ khai, 2 chỗ là rác chết ⛔ không áp, còn 46 màn bó thật)*.

Hai kỷ luật đo:
- Hệ có trạng thái **dao động** thì **đo một lần là kết luận sai**. Gặp `warn`/`offline`/`timeout` phải đo lại nhiều lượt cách nhau vài giây.
- Đo **CORS** phải đo **trong trình duyệt**: `curl` ⛔ không chịu ràng buộc CORS nên không bao giờ báo lỗi.

**Lớp 4 · QUY ƯỚC.** Timecode · header `**Soạn:** P<số> · **THỰC HIỆN: Leader**` · nhật ký Code · todolist `- [ ]` · dòng "Hoàn thành Plan lúc" · liên kết chéo tới đích còn tồn tại · **⛔ không có gạch dài**.

## Bảng loại lỗi (rút từ hơn 40 ca thật)

| Nhóm | Dấu hiệu | Ca thật |
|---|---|---|
| Tự phá mục tiêu | Cách làm không đạt chính mục tiêu Plan nêu | trang mỏng chuyển hướng nằm trong bó một khối |
| Đảo nghĩa | Rơi mất "KHÔNG"/"⛔"/"chưa" | *"Plan này ⛔ dùng được cho tới khi…"* |
| Số bịa | Tiêu chí nghiệm thu không nguồn đo | "dưới 300 KB" thấp hơn cả hai app thật |
| Số lỗi thời | Chép từ memory cũ | 1/66 dự án (thật 2/72) · 32 hàm (thật 39) |
| Số sai đơn vị | Nhầm phần này với phần kia | "mô hình 1,6 MB" (thật 1,6 mã + 8,8 mô hình) |
| Mâu thuẫn hai mục | Cùng tệp nói hai số khác nhau *(⚠️ đếm thật trước khi gọi là lỗi)* | "17 GB" vs "14,4 GB" |
| Mâu thuẫn do lượt vá | Vá chỗ này quên chỗ kia | vừa sửa tệp vừa bảo gỡ tệp đó |
| Tính năng bỏ sót | Thứ đang chạy thật mà đặc tả không nhắc | mật khẩu link, thẻ xem trước khi chia sẻ link |
| Tham chiếu chết | Trỏ mục đã đổi tên/nội dung | "xem mục 4b" |
| Mốc bất khả thi | Nghiệm thu dựa vào thứ sẽ hết hạn | "mở cả bốn link" (2 link chết sau 3 ngày) |
| Tưởng dùng lại được | Hàm ở **kho git khác** | một hàm ở kho app, web không import được |
| Việc thừa | Bảo làm thứ nền tảng tự lo | "thêm app vào turbo" |
| Thiếu ranh giới | Plan bàn giao chéo không nói đụng tệp nào | một Plan bàn giao chéo thiếu hẳn mục ranh giới |

## Ranh giới: tự sửa vs HỎI

| Tự sửa ngay | Phải HỎI user |
|---|---|
| Hình thức, đánh số mục, tham chiếu chết, gạch dài, lỗi gõ | Đổi **phạm vi** Plan (thêm/bớt việc) |
| Số sai hoặc lỗi thời (ghi rõ *"đo lại ngày…"*) | Đổi **cách làm** đã chốt |
| Mâu thuẫn khi **đã biết vế nào đúng** | Mâu thuẫn mà **chưa rõ vế nào đúng** |

🔴 **Ngưỡng NÊN VIẾT LẠI:** nếu một vòng ra **quá 5 lỗi thiết kế** (không tính hình thức và số liệu), dừng vá và **hỏi user có nên viết lại Plan** thay vì chắp vá tiếp.

## Vòng lặp và tiêu chí PASS

- 🔴 **Mỗi vòng gọi `Agent` `subagent_type: "roleflow:PlanReviewer"` MỚI**. Tin gọi: đường dẫn Plan, Idea đi kèm, số vòng, các lớp cần chạy, mục vòng trước đã sửa.
  *(Vì sao: tự rà báo PASS mà trợ lý độc lập vẫn ra 8 lỗi; lượt vá đẻ lỗi mới.)*
  Phiên chính giữ: hỏi user các câu agent trả về · đếm vòng, trần · ghi mục VÒNG RÀ vào Idea · đóng dấu PASS.
- **Plan nhỏ** (ít số liệu, dưới ~100 dòng): chạy **lớp 1 + 2 + 4**, bỏ lớp 3. Thường 1 tới 2 vòng là xong.
- **Plan lớn / có nhiều số đo**: chạy đủ 4 lớp.
- **Vòng sau chạy lớp nào tuỳ vòng trước sửa gì**: sửa số → chạy lại lớp 3 · sửa câu chữ → chạy lại lớp 2 · **vòng chốt luôn là lớp 4**. ⛔ Đừng chạy đủ 4 lớp mỗi vòng, đắt vô ích.
- 🔴 **Từ vòng 2 chỉ đọc mục vừa sửa** *(PlanReviewer ăn 14.3% quota)*:
  tin gọi ghi **khoảng dòng** các mục vòng trước đã sửa cộng **lỗi của mọi vòng trước**. Agent ⛔ không báo lại lỗi đã báo;
  lỗi mới ở chỗ ⛔ không sửa thì ghi Nhẹ. **Lớp 2 đọc trọn Plan đúng một lần, ở vòng chốt** *(bắt lỗi lan ra ngoài chỗ sửa)*.
- 🔴 **Gom theo loại**: mỗi lỗi ghi `loại`; agent `rg` tìm mọi chỗ cùng mẫu trong Plan và sửa một lượt, ⛔ đừng để vòng sau bắt nốt.
- 🔴 **Trần 3 vòng rồi HỎI**: hết vòng 3 mà vẫn ra lỗi thì DỪNG, báo user đã chạy mấy vòng, bắt được bao nhiêu,
  **hỏi đi tiếp hay xem lại cách viết Plan**. User bảo đi tiếp thì mỗi lần thêm tối đa 3 vòng rồi hỏi lại. ⛔ Không im lặng kết thúc khi chưa hội tụ.

**PASS khi đủ 6 điều:**
1. Mọi con số **có nguồn đo**, hoặc ghi rõ là ước lượng
2. Mọi tham chiếu chéo trỏ tới mục **còn tồn tại**
3. Không có hai chỗ nói **hai số khác nhau** cho cùng một thứ *(⚠️ đã **đếm thật** để loại khả năng chúng đo hai thứ khác nhau)*
4. Mọi mốc nghiệm thu **thực hiện được** (không dựa vào thứ sẽ hết hạn)
5. Đủ quy ước lớp 4, **0 gạch dài**
6. Plan **bàn giao chéo** có mục **ranh giới tệp**

## Ghi kết quả

- **Ghi vào Idea đi kèm** một mục `## <n>. VÒNG RÀ …` liệt kê lỗi và lý do sửa. Idea ở lại vĩnh viễn nên đó là chỗ đúng; Plan chỉ mang bản đã sửa.
  ⚠️ **Plan ⛔ KHÔNG có Idea đi kèm** thì ghi mục VÒNG RÀ **vào cuối chính Plan**, ⛔ đừng tự tạo file Idea mới và ⛔ đừng bỏ không ghi.
- **Đóng dấu đầu Plan**: `🔎 Đã rà <N> vòng lúc <YYYY-MM-DD HH:MM> · PASS` để phiên sau khỏi rà lại từ đầu.
- **PASS thì chuyển dòng** `activerole.py index move <tc> Plan_Draft Plan_Pass` *(thế là bàn giao Leader, ⛔ không cần nhắn)*; nhắc memory liên quan nếu nội dung đổi.
  Đọc mã ở **dòng 1**: phải là `DA_CHUYEN`; `NHIEU_DONG` thì gọi lại bằng đường ở dòng `DONG`; `KHONG_THAY_DONG` *(Plan ⛔ không có dòng trong `Plan_Draft`)* hay mã lỗi khác thì DỪNG, báo user.
- Rà ⛔ không PASS mà bỏ dở *(user dừng, chưa đi tiếp sau trần 3 vòng)* thì nhả ô: `activerole.py index release <tc> <mã>` *(phải ra `DA_NHA`)*.
- **Nhắc mốc hỏi xuất HTML**: viết xong Plan là một trong hai mốc phải mời user `/roleflow:exportplan`.

## Lưu ý riêng

- **Plan bàn giao chéo** (`THỰC HIỆN` ≠ `Soạn`): soi kỹ hơn phần **ranh giới tệp** và **hotspot phải hỏi trước khi sửa**, vì người code không phải người viết.
- **Master + sub-plan**: rà Master thì soi *điều phối* (thứ tự, phụ thuộc, ai làm gì); rà sub thì soi *đặc tả*. ⛔ Đừng lẫn.
- ⚡ **Kỷ luật token:** chỉ đọc Plan đang rà và Idea của nó, ⛔ không đọc Plan khác. Lớp 3 và 4 chỉ dùng `grep`.

## Báo cáo cuối
Bảng *từng vòng bắt được bao nhiêu* · **ba lỗi nặng nhất** · trạng thái cuối (số dòng, gạch dài, todolist, PASS hay chưa) · việc còn chờ user.

## Chế độ Idea *(tệp nằm trong `01_IDEA/Idea_List/`)*
- Chỉ **hai lớp**: **khả thi** (lớp 1 trên từng chốt: làm được, đo được ⛔ không) · **mâu thuẫn** (lớp 2: chốt chỏi chốt, chỏi Plan đã link). Bỏ lớp 3, 4.
- Tin gọi `roleflow:PlanReviewer` dặn: ⛔ **không sửa chốt** (câu đã chốt, phương án loại), chỉ báo để phiên chính hỏi user; tự sửa chỉ lỗi gõ, tham chiếu chết.
- Mục `VÒNG RÀ` ghi cuối chính Idea, dấu 🔎 đầu Idea; trần vòng như Plan. PASS: `activerole.py index move <tc> Idea_Draft Idea_Pass`; đọc mã dòng 1 như Plan *(`DA_CHUYEN`; `KHONG_THAY_DONG` hay mã lỗi khác thì DỪNG, báo user)*.
