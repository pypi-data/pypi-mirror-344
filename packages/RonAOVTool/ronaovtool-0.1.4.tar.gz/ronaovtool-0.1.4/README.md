## Cài đặt
```python
pip install RonAOVTool
```
## Giới thiệu
- `RonAOVTool.hashcode()` của RonAOVTool giúp chuyển đổi từ chuỗi thành mã băm theo định dạng của AOV.
- Trong `RonAOVTool` có hỗ trợ `RonAOVTool.load(filename)` để đọc file Assetbundle chưa mã hóa, `filname` sẽ thay bằng đường dẫn tới tệp Assetbundle.
- Tích hợp `.changePath(original_path, new_path)` để thay đổi đường dẫn đã có sẵn trong AOV thành đường dẫn mới, với các giá trị truyền vào phải là chuỗi và không cần đuôi tệp.
- Cuối cùng là `.save()` để lưu những thay đổi của tệp Assetbundle.
## Cách dùng
```python
import RonAOVTool as tool

file = tool.load('test.assetbundle')
file.changePath('test/path/1', 'test/path/2')
file.save()

print(tool.hashcode("đây là chuỗi sẽ chuyển thành mã băm"))
```
## Thông tin tác giả
© Thư viên do [Ron AOV](https://youtube.com/@ronaov) thực hiện