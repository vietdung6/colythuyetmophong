import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Tạo figure và các trục
fig = plt.figure(figsize=(12, 5))
ax1 = fig.add_subplot(121)  # Đồ thị thế năng hiệu dụng
ax2 = fig.add_subplot(122, projection='polar')  # Đồ thị quỹ đạo (dùng tọa độ cực)

# Các thông số ban đầu
M_init = 1.0    # Moment động lượng góc
m_init = 1.0    # Khối lượng
E_init = 0.5    # Năng lượng toàn phần

# Tính r_min
def calculate_r_min(M, m, E):
    return M / np.sqrt(2 * m * E)

# Tính thế năng hiệu dụng
def effective_potential(r, M, m):
    return (M**2) / (2 * m * r**2)

# Tính quỹ đạo r(phi)
def orbit_equation(phi, M, m, E):
    return M / (np.sqrt(2 * m * E) * np.cos(phi))

# Vẽ đồ thị thế năng hiệu dụng
def plot_potential(M, m, E):
    r_min = calculate_r_min(M, m, E)
    r = np.linspace(r_min * 0.5, r_min * 5, 1000)
    U_hd = effective_potential(r, M, m)
    
    ax1.clear()
    ax1.plot(r, U_hd, 'b-', linewidth=2)
    ax1.axhline(y=E, color='r', linestyle='--', label='E')
    ax1.axvline(x=r_min, color='g', linestyle='--', label='r_min')
    
    # Đánh dấu điểm giao nhau
    ax1.plot(r_min, E, 'ro')
    
    # Thêm nhãn và tiêu đề
    ax1.set_xlabel('r')
    ax1.set_ylabel('U_hd')
    ax1.set_title('Thế năng hiệu dụng')
    ax1.text(r_min * 3, E * 0.5, f'$\\frac{{M^2}}{{2mr^2}}$', fontsize=12)
    
    # Giới hạn trục y
    ax1.set_ylim(0, max(2 * E, np.max(U_hd[:int(len(U_hd)/3)])))
    ax1.grid(True)
    ax1.legend(loc='upper right')  # Đặt legend ở góc trên bên phải

# Vẽ đồ thị quỹ đạo
def plot_orbit(M, m, E):
    r_min = calculate_r_min(M, m, E)
    
    # Tránh phi quá gần pi/2 để tránh r tiến đến vô cùng
    max_phi = np.pi/2 - 0.1
    phi = np.linspace(-max_phi, max_phi, 1000)
    r = orbit_equation(phi, M, m, E)
    
    ax2.clear()
    ax2.plot(phi, r, 'b-', linewidth=2)
    
    # Đánh dấu r_min tại phi=0
    ax2.plot(0, r_min, 'ro', markersize=8)
    
    # Vẽ vòng tròn r=r_min trong tọa độ cực
    theta = np.linspace(0, 2*np.pi, 100)
    ax2.plot(theta, np.ones_like(theta)*r_min, 'g--', alpha=0.7)
    
    # Cài đặt hiển thị
    ax2.set_title('Quỹ đạo chuyển động')
    ax2.grid(True)
    
    # Giới hạn bán kính hiển thị
    max_r = np.min([5 * r_min, np.max(r[np.isfinite(r)])])
    ax2.set_rmax(max_r)

# Vẽ cả hai đồ thị với giá trị ban đầu
plot_potential(M_init, m_init, E_init)
plot_orbit(M_init, m_init, E_init)

# Thêm thanh trượt để điều chỉnh tham số
plt.subplots_adjust(bottom=0.25)
ax_M = plt.axes([0.25, 0.1, 0.65, 0.03])
ax_E = plt.axes([0.25, 0.15, 0.65, 0.03])

slider_M = Slider(ax_M, 'M', 0.1, 2.0, valinit=M_init)
slider_E = Slider(ax_E, 'E', 0.1, 2.0, valinit=E_init)

# Tạo text box hiển thị r_min ở vị trí riêng biệt
r_min_text = plt.figtext(0.5, 0.02, f'r_min = {calculate_r_min(M_init, m_init, E_init):.3f}', 
                        ha='center', fontsize=12, bbox=dict(facecolor='lightblue', alpha=0.5))

# Hàm cập nhật khi thay đổi tham số
def update(_):
    M = slider_M.val
    E = slider_E.val
    r_min = calculate_r_min(M, m_init, E)
    
    plot_potential(M, m_init, E)
    plot_orbit(M, m_init, E)
    
    # Cập nhật giá trị r_min
    r_min_text.set_text(f'r_min = {r_min:.3f}')
    
    fig.canvas.draw_idle()

# Đăng ký hàm cập nhật
slider_M.on_changed(update)
slider_E.on_changed(update)

# Thêm thông tin phương trình
plt.figtext(0.5, 0.04, 'Phương trình quỹ đạo: r = M/(√(2mE)cos(φ))', ha='center', fontsize=10)
plt.figtext(0.02, 0.95, 'Điểm ngoặt: E - U_hd = 0 ⟹ E = M²/(2mr²) ⟹ r_min = M/√(2mE)', fontsize=9)
plt.figtext(0.02, 0.92, 'Điều kiện tồn tại chuyển động: E ≥ U_hd ⟹ r ≥ r_min', fontsize=9)

plt.tight_layout(rect=[0, 0.2, 1, 0.9])
plt.suptitle('Mô phỏng chuyển động trong trường lực xuyên tâm', fontsize=16)
plt.show()
