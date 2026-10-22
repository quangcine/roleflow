# start · phần riêng Planner

Đọc tệp này **chỉ khi** skill `roleflow:start` đã chọn vai Planner. `A` và `Roles.md` dùng đúng đường thật đã định ở `SKILL.md` của skill này (tệp này đọc bằng `Read` nên biến đường plugin ⛔ không được thay; ⛔ không tự ghép đường). Quyền Planner: `Roles.md` mục Planner
*(⛔ không code, ⛔ không commit, ⛔ không giao việc, ⛔ không ghi memory)*.

## Chọn việc *(khi ⛔ không nhận nợ)*
Đi lần lượt bốn bậc; bậc nào có dòng thì hỏi ở bậc đó, chủ dự án chọn *xem bậc sau* thì đi tiếp.
Mỗi bậc chạy `python3 $A index list <sổ> --free` → dòng `MUC<TAB>tc<TAB>đường<TAB>Tên<TAB>ô Đang cầm`, cuối là `SO_DONG <n>`
*(chỉ dòng có ô Đang cầm trống)*. Đọc trường bằng `cut -f2,3,4` hoặc `awk -F'\t'`; ⛔ không dùng `IFS read`. `RONG <sổ>` hoặc `SO_DONG 0` thì sang bậc sau.

| Bậc | Sổ | Hỏi | Nhận rồi làm |
|---|---|---|---|
| 1 | `Plan_Draft` | rà Plan nào | `/roleflow:reviewplan`; PASS thì skill đó chuyển dòng sang `Plan_Pass` |
| 2 | `Idea_Pass` | viết Plan nào từ Idea nào | viết Plan, thêm dòng `index add Plan_Draft --value "<dòng>"`, xong Plan đầu tiên thì `index move <tc> Idea_Pass Idea_Done` |
| 3 | `Idea_Draft` | rà hay viết tiếp Idea nào | `/roleflow:reviewplan` chế độ Idea; PASS thì chuyển sang `Idea_Pass` |
| 4 | *(hết)* | có ý tưởng mới không | ghi Idea mới, thêm dòng `index add Idea_Draft --value "<dòng>"` |

- Hỏi bằng `AskUserQuestion`: *Tên* kèm *tc*, cộng lựa chọn *xem bậc sau* và *việc khác*.
- **Nhận việc**: `python3 $A index hold <đường> <mã>` *(đường = trường 3)* TRƯỚC khi đọc tệp.
  `DA_CO_NGUOI_CAM`: Planner khác vừa nhận, hỏi chọn lại. `NHIEU_DONG`: gọi lại bằng đường ở dòng `DONG` đã chọn. Mã lỗi khác thì DỪNG, báo user.
- Rồi `python3 $A note <mã> <ts> "<việc>"`. Đọc tệp: nối `GOC=` của `show` với *đường*.
- Bỏ việc giữa chừng mà ⛔ không rời vai: `python3 $A index release <đường> <mã>` *(phải ra `DA_NHA`)*.
- `index add`, `index move` cũng đọc mã ở **dòng 1**: phải là `DA_THEM`, `DA_CHUYEN`; `NHIEU_DONG` gọi lại bằng đường ở dòng `DONG`; mã lỗi khác *(`KHONG_THAY_DONG`, `DA_CO_DONG`, `CHUYEN_SAI`…)* thì DỪNG, báo user.

## Nhắc khi làm
- Đầu Plan ghi `**Soạn:** <mã> · **THỰC HIỆN: Leader**`.
- Chuyển dòng chỉ phần của Planner *(bảng trong `Roles.md` mục Planner)*; `Plan_Pass` → `Plan_Done`, `Plan_Cancel`, `Plan_Debt` và `Plan_Draft` → `Plan_Debt` là việc Leader.
- ⛔ Không đọc `Plan_Debt` *(nợ dài hạn)*, ⛔ không `index list Plan_Debt`, trừ khi chủ dự án hỏi.
- Một câu chốt chỉ một phiên hỏi: câu thuộc Plan nào thì người đang cầm Plan đó hỏi.
