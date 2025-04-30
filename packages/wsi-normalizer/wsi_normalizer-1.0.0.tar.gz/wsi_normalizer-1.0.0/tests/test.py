import cv2
from wsi_normalizer import MacenkoNormalizer, ReinhardNormalizer, VahadaneNormalizer

# 定义读取图像的函数
def read_image(path):
    im = cv2.imread(path)
    im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
    return im

# 设置图像路径
img_path = 'eg_slide_1/eg_1.jpg'
target_path = 'eg_slide_1/eg_2.jpg'

# 读取图像
img = read_image(img_path)
target = read_image(target_path)

# 初始化归一化器
mnormalizer = MacenkoNormalizer()
rnormalizer = ReinhardNormalizer()
vnormalizer = VahadaneNormalizer()

# 拟合归一化器
mnormalizer.fit(img)
rnormalizer.fit(img)
vnormalizer.fit(img)

# 对目标图像进行归一化
m = mnormalizer.transform(target)
r = rnormalizer.transform(target)
v = vnormalizer.transform(target)

# 保存归一化后的图像
cv2.imwrite('m.jpg', cv2.cvtColor(m, cv2.COLOR_RGB2BGR))
cv2.imwrite('r.jpg', cv2.cvtColor(r, cv2.COLOR_RGB2BGR))
cv2.imwrite('v.jpg', cv2.cvtColor(v, cv2.COLOR_RGB2BGR))
