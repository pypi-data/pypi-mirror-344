# scient

**scient**一个用python实现科学计算相关算法的包，包括自然语言、图像、神经网络、优化算法、机器学习、图计算等模块。

**scient**源码和编译安装包可以在`Python package index`获取。

The source code and binary installers for the latest released version are available at the [Python package index].

[https://pypi.org/project/scient](https://pypi.org/project/scient)

可以用`pip`安装`scient`。

You can install `scient` like this:
    
```
pip install scient
```

也可以用`setup.py`安装。

Or in the `scient` directory, execute:

```
python setup.py install
```

## scient.image

图像相关算法模块，包括边缘检测、图像相似度计算、图像质量评价、图像特征提取等。

### scient.image.friqa

全参考图像质量评价模块，包括峰值信噪比（PSNR），结构相似度（SSIM），直方图相似度（HistSim）。

#### scient.image.friqa.psnr(image1,image2,max_pix=255)

Parameters
----------
image1 : numpy.array 2D or 3D，参考图像

image2 : numpy.array 2D or 3D，待评价图像

max_pix : int, optional default is 255, 像素值的最大值，默认值是255.

Returns
-------
float

Algorithms
-------
PSNR(Peak Signal to Noise Ratio)，峰值信噪比，是一种评价图像的客观标准，单位dB。图像在经过压缩之后，会在某种程度与原始图像不同，PSNR值用来衡量经过处理后的图像品质是否令人满意。

$$
PSNR=10 \cdot \log _ {10} ( \frac { MAX _ I ^ 2 } { MSE }) = 20 \cdot \log _ {10} ( \frac { MAX _ I } { MSE })
$$

其中，$MAX _ I$是图像像素值的最大值，一般每个采样点用8位表示，那么$MAX _ I$就是255。

$MSE$是待评价图像与参考图像的均方误差，$MSE$越小，PSNR越大；PSNR越大，待评价图像质量越好。

* PSNR高于40dB说明待评价图像质量极好,非常接近原始图像；
* PSNR在30—40dB说明待评价图像质量是较好，虽然有明显失真但可以接受；
* PSNR在20—30dB说明待评价图像质量差；
* PSNR低于20dB说明待评价图像质量不可接受。


PSNR缺点：基于对应像素点间的误差，即基于误差敏感的图像质量评价。由于并未考虑到人眼的视觉特性（人眼对空间频率较低的对比差异敏感度较高，人眼对亮度对比差异的敏感度较色度高，人眼对一个 区域的感知结果会受到其周围邻近区域的影响等），因而经常出现评价结果与人的主观感觉不一致的情况。

Examples
-------

```
import os
from scient.image import friqa
import numpy
from PIL import Image

ref_image='test/data/I10.BMP'
images=['test/data/I10.BMP','test/data/i10_23_3.bmp','test/data/i10_23_4.bmp','test/data/i10_23_5.bmp','test/data/i10_24_5.bmp']

#读取图像文件
ref_image=Image.open(os.path.join(os.path.dirname(friqa.__file__),'..',ref_image))
images=[Image.open(os.path.join(os.path.dirname(friqa.__file__),'..',i)) for i in images]

#计算psnr
for i in images:
    print(friqa.psnr(numpy.array(ref_image),numpy.array(i)))
```

运行结果

```
100
32.436263852012544
31.184291262813648
30.272831107297733
29.3584810257951
```
    
    
#### scient.image.friqa.ssim(image1,image2,k1=0.01,k2=0.03,block_size=(8, 8),max_pix=255)

Parameters
----------
image1 : numpy.array 2D

image2 : numpy.array 2D

k1 : float, optional，k1<<1,避免分母为0造成不稳定. The default is 0.01.

k2 : float, optional，k2<<1,避免分母为0造成不稳定. The default is 0.03.

block_size : tuple, optional，将图像分成多个block,采用gaussian加权计算所有block的均值、方差、协方差,进而计算所有block的ssim,最后的ssim取所有block的平均值. The default is (8,8).

max_pix : int, optional default is 255, 像素值的最大值，默认值是255.

Returns
-------
float

Algorithms
-------

SSIM(Structural Similarity)，结构相似度，用于衡量两个图像相似程度，或检测图像的失真程度。
SSIM基于样本之间的亮度(luminance,像素平均值)、对比度(contrast,像素标准差)和结构(structure,像素减均值除以标准差)计算。

$$
SSIM(x,y)=f(l(x,y),c(x,y),s(x,y))
$$

$l(x,y)$为亮度对比函数，是关于图像的平均灰度$μ_x,μ_y$的函数；

$$
l(x,y)=\frac { 2μ_x μ_y + C1 } { μ_x^2 μ_y^2 + C1 }
$$

$$
μ_x=\frac { 1 } { N } \sum^{N}_{i=1}{x_i}
$$

$$
C1=(K_1 L)^2
$$

像素值的最大值，默认值是255. K1<<1。

$c(x,y)$为对比度对比函数，是关于图像的标准差$σ_x,σ_y$的函数；

$$
c(x,y)=\frac { 2σ_x σ_y + C2 } { σ_x^2 σ_y^2 + C2 }
$$

$$
σ_x=(\frac { 1 } { N-1 } \sum^{N}_{i=1}{(x_i-μ_x)^2})^{\frac { 1 } { 2 }}
$$

$$
C2=(K_2 L)^2
$$

K2<<1

$s(x,y)$为结构对比函数，是关于图像的标准化$\frac { x-μ_x } { σ_x },\frac { y-μ_y } { σ_y }$的函数；

$$
s(x,y)=\frac { σ_{xy} + C3 } { σ_x σ_y + C3 }
$$

$$
σ_{xy}=\frac { 1 } { N-1 } (\sum^{N}_{i=1}{(x_i-μ_x)(y_i-μ_y)})
$$

$$
SSIM(x,y)=[l(x,y)]^α[c(x,y)]^β[s(x,y)]^γ
$$

α,β,γ取1，令$C_3=\frac { C_2 } { 2 }$，可将SSIM简化为：

$$
SSIM(x,y)=\frac { (2μ_x μ_y + C1)(2σ_{xy} + C2) } { (μ_x^2 μ_y^2 + C1)(σ_x^2 σ_y^2 + C2) }
$$

SSIM取值范围为[0,1]，值越大表示图像质量越好。
SSIM具有：对称性，ssim(x,y)==ssim(y,x);
         有界性,ssim(x,y)<=1;
         最大值唯一性，当且仅当x==y时，ssim(x,y)==1。
SSIM缺点：对于图像出现位移、缩放、旋转（皆属于非结构性的失真）的情况无法有效的判断。

Examples
-------

```
import os
from scient.image import friqa
import numpy
from PIL import Image

ref_image='test/data/I10.BMP'
images=['test/data/I10.BMP','test/data/i10_23_3.bmp','test/data/i10_23_4.bmp','test/data/i10_23_5.bmp','test/data/i10_24_5.bmp']

#读取图像文件
ref_image=Image.open(os.path.join(os.path.dirname(friqa.__file__),'..',ref_image))
images=[Image.open(os.path.join(os.path.dirname(friqa.__file__),'..',i)) for i in images]

#计算ssim
for i in images:
    print(friqa.ssim(numpy.array(ref_image.convert("L")),numpy.array(i.convert("L"))))
```

运行结果

```
1.0
0.8568124416229375
0.6810351495300123
0.5575398637742431
0.5072153083460104
```

#### scient.image.friqa.histsim(image1,image2,channel_first = False)

Parameters
----------
image1 : numpy.array 2D or 3D

image2 : numpy.array 2D or 3D

channel_first : bool, optional, channel是否在第1维上

Returns
-------
float

Algorithms
-------
直方图相似度是按照距离度量的标准对两幅图像的直方图进行相似度的测量。
取值范围为[0,1]，值越大表示图像越相似。
优点：计算量比较小。
缺点： 直方图反应的是图像灰度值得概率分布，并没有图像的空间位置信息在里面，因此，会出现误判；比如纹理结构相同，但明暗不同的图像，应该相似度很高，但实际结果是相似度很低，而纹理结构不同，但明暗相近的图像，相似度却很高。

Examples
-------

```
import os
from scient.image import friqa
import numpy
from PIL import Image

ref_image='test/data/I10.BMP'
images=['test/data/I10.BMP','test/data/i10_23_3.bmp','test/data/i10_23_4.bmp','test/data/i10_23_5.bmp','test/data/i10_24_5.bmp']

#读取图像文件
ref_image=Image.open(os.path.join(os.path.dirname(friqa.__file__),'..',ref_image))
images=[Image.open(os.path.join(os.path.dirname(friqa.__file__),'..',i)) for i in images]

#计算histsim
for i in images:
    print(friqa.histsim(numpy.array(ref_image),numpy.array(i)))
```

运行结果

```
1.0
0.8446511435120678
0.7827152024090115
0.7333089200530448
0.6737696532004112
```


### scient.image.feature

图像特征提取模块，包括BRISQUE，基于累积概率的锐化因子（CPB），曝光度。

#### scient.image.feature.brisque(image)

Parameters
----------
image : numpy.array 2D

Returns
-------
tuple
('gdd_α','gdd_σ',
'aggd_α1','aggd_η1','aggd_σl1','aggd_σr1',
'aggd_α2','aggd_η2','aggd_σl2','aggd_σr2',
'aggd_α3','aggd_η3','aggd_σl3','aggd_σr3',
'aggd_α4','aggd_η4','aggd_σl4','aggd_σr4')

Algorithms
-------
 BRISQUE（Blind/Referenceless Image Spatial QUality Evaluator），是一种无参考的空间域图像质量评估算法。先计算Mean Subtracted Contrast Normalized Coefficients（MSCN系数），MSCN系数反映了由于失真的存在而改变的特征统计，可以用来作为图像失真的统计特征。再用MSCN系数估计Generalized Gaussian Distribution（GDD）的参数α、σ，以及Asymmetric Generalized Gaussian Distribution（AGGD）在Horizontal Neighbour, Vertical Neighbour, On Diagonal Neighbour, Off Diagonal Neighbour上的参数α、η、σl、σr，将GDD的两个参数和AGGD的16个参数作为输出的特征。

MSCN系数：

$$
MSCN(i,j)=\frac { I(i,j)-μ(i,j) } { σ(i,j)+C }
$$

$$
μ(i,j)=\sum^{K}_{k=-K}{\sum^{L}_{l=-L}{w_{k,l}I_{k,l}(i,j)}}
$$

$$
σ(i,j)=\sqrt{\sum^{K}_{k=-K}{\sum^{L}_{l=-L}{w_{k,l}(I_{k,l}(i,j)-μ(i,j))^2}}}
$$

其中$I(i,j)$表示原始图像i行j列元素的值。

Generalized Gaussian Distribution：

$$
f(x;α,σ^2)=\frac {α} {2βΓ(1/α)} e^{-(\frac {|x|}{β})^α}
$$

$$
β=σ\sqrt{\frac{Γ(1/α)}{Γ(3/α)}}
$$

$$
Γ(α)=\int^{\infty}_{0}{t^{α-1}e^{-t}dt} α>0
$$

Neighbours:

$$
HorizontalNeighbour(i,j)=MSCN(i,j)MSCN(i,j+1)
$$

$$
VerticalNeighbour(i,j)=MSCN(i,j)MSCN(i+1,j)
$$

$$
OnDiagonalNeighbour(i,j)=MSCN(i,j)MSCN(i+1,j+1)
$$

$$
OffDiagonalNeighbour(i,j)=MSCN(i,j)MSCN(i+1,j-1)
$$

Asymmetric Generalized Gaussian Distribution:

$$
f(x;α,σ_l^2,σ_r^2)=
\frac {α}{(β_l+β_r)Γ(1/α)}e^{-(\frac {-x}{β_l})^α} x<0
\frac {α}{(β_l+β_r)Γ(1/α)}e^{-(\frac {x}{β_r})^α} x>=0
$$

$$
β_l=σ_l\sqrt{\frac{Γ(1/α)}{Γ(3/α)}}
$$

$$
β_r=σ_r\sqrt{\frac{Γ(1/α)}{Γ(3/α)}}
$$

Examples
-------

```
import os
from scient.image import feature
import numpy
from PIL import Image

images=['test/data/I10.BMP','test/data/i10_23_3.bmp','test/data/i10_23_4.bmp','test/data/i10_23_5.bmp','test/data/i10_24_5.bmp']

#读取图像文件
images=[Image.open(os.path.join(os.path.dirname(feature.__file__),'..',i)) for i in images]

#计算brisque
brisques=[]
for i in images:
    brisques.append(feature.brisque(numpy.array(i.convert('L'))))
print(brisques)
```

运行结果

```
[(2.8390000000000026, 0.5387382509471336, 0.8180000000000005, 0.1597336483186561, 0.19928197982139934, 0.4696747920784309, 0.8640000000000005, 0.17081167501931036, 0.1703080506100513, 0.440894038756712, 0.8610000000000007, -0.002437981115828319, 0.2983089768677447, 0.2943996123553127, 0.8670000000000007, 0.03657370089459203, 0.2641503963750437, 0.32229688865209727), (2.179000000000002, 0.3755805588864052, 0.6610000000000005, 0.2105638785869636, 0.06573065885425396, 0.3546433105372317, 0.7250000000000005, 0.2035633011201771, 0.04895566298941261, 0.2895746994148656, 0.7110000000000005, 0.09196294223642214, 0.10660221933416321, 0.22150476223116147, 0.7220000000000004, 0.10061626044729756, 0.09951649928883519, 0.22307536755643081), (1.489000000000001, 0.19567592119387475, 0.4370000000000002, 0.16656579278574843, 0.005144811587270607, 0.1595102390164801, 0.4400000000000002, 0.14819323960693676, 0.007946536338563829, 0.14400949152877282, 0.46900000000000025, 0.1304195444573072, 0.010840852166168865, 0.12285748598680354, 0.47300000000000025, 0.12785146234621667, 0.011051488263507676, 0.11939877242752284), (1.2570000000000008, 0.1189807661854071, 0.2940000000000001, 0.09858069094224381, 0.0033503171775502846, 0.1003980673321924, 0.2960000000000001, 0.09662228540309649, 0.0037953392707882772, 0.09854664422093222, 0.3160000000000001, 0.08840261656054116, 0.004225987220008733, 0.08029184471742051, 0.3180000000000001, 0.08631426420092875, 0.004399447310061135, 0.07751730107145516), (1.203000000000001, 0.14103130545847511, 0.3270000000000001, 0.10623288442963101, 0.008919473174326557, 0.12226537626029133, 0.3280000000000001, 0.06853644417080812, 0.02378947796849877, 0.10143999168472712, 0.33900000000000013, 0.05689116726400874, 0.02385946076111514, 0.08256978072093775, 0.33900000000000013, 0.05450324427873719, 0.02492368706293601, 0.0813272014967197)]
```

#### scient.image.feature.cumprob(image)

Parameters
----------
image : numpy.array 2D

Returns
-------
float

Algorithms
-------

基于累积概率的锐化因子（Cumulative Probability of Blur, CPB），是一种无参考的图像锐化定量指标评价因子,基于模糊检测的累积概率来进行定义。
根据人类视觉的特点，建立可察觉失真模型（Just Noticeable Distortion Model， JND），通过建模人眼能够察觉的图像底层特征，只有超过一定的阈值才会被察觉为失真图像。如果在空间域计算，一般会综合考虑亮度，纹理等因素，比如用像素点处局部平均背景亮度值作为亮度对比度阈值，用各个方向的梯度作为纹理阈值。如果在变换域计算，则可以使用小波系数等。
在给定一个对比度高于JND (Just Noticeable Distortion)参考的情况下，定义JNB (Just Noticeable Blur)指标为感知到的模糊像素的最小数目，边缘处像素的模糊概率定义如下：

$$
P_{blur}=P(e_i)=1-e^{-|\frac {ω(e_i)}{ω_{jnb}(e_i)_}|^β}
$$

其中分子是基于局部对比度的JNB边缘宽度，而分母是计算出的边缘宽度。对于每一幅图像，取一定大小的子块，然后将其分为边缘块与非边缘块，非边缘块不做处理。对于每一个边缘块，计算出块内每个边缘像素的宽度。当Pblur超过一定阈值时，该像素即作为有效的像素，用于计算CPB指标：

$$
CPBD=P(P_{blur}<=P_{jnb})=\sum^{P_{blur}=P_{jnb}}_{P_{blur}=0}{P(P_{blur})}
$$

CPB符合人类视觉特性的图像质量指标，值越大，所反映出的细节越清晰，模糊性越弱。因此，可以将此指标用于定量评判滤波后的图像的锐化质量。

Examples
-------

```
import os
from scient.image import feature
import numpy
from PIL import Image

images=['test/data/I10.BMP','test/data/i10_23_3.bmp','test/data/i10_23_4.bmp','test/data/i10_23_5.bmp','test/data/i10_24_5.bmp']

#读取图像文件
images=[Image.open(os.path.join(os.path.dirname(feature.__file__),'..',i)) for i in images]

#计算cumprob
for i in images:
    print(feature.cumprob(numpy.array(i.convert('L'))))
```

运行结果

```
0.7780217681878938
0.3778794572420322
0.11440817672271678
0.07692307692307693
0.19828178694158077
```

### scient.image.hash

图像hash模块，包括均值hash(mean hash),差值hash(diff hash),感知hash(percept hash)。

#### scient.image.hash.percept(image,hash_size=64)

Parameters
----------
image : numpy.array 2D

hash_size : 输出hash值的长度

Returns
-------
list

Algorithms
-------
先将图片缩放成hash_size*hash_size大小，然后对图像进行离散余弦变换DCT，并输出左上角h*w=hash_size的mean hash。
DCT是一种特殊的傅立叶变换，将图片从像素域变换为频率域，并且DCT矩阵从左上角到右下角代表越来越高频率的系数，图片的主要信息保留左上角的低频区域。

一维DCT变换：

$$
F(x)=c(x)\sum^{N-1}_{i=0}{f(i)cos(\frac {(i+0.5)π}{N}x) }
$$

$$
c(x)=\left\{\begin{matrix}\sqrt{\frac{1}{N}} ,x=0\\\sqrt{\frac{2}{N}} ,x!=0 \end{matrix}\right.
$$

f(i)为原始的信号，F(x)是DCT变换后的系数，N为原始信号的点数，c(x)是补偿系数。

二维DCT变换：

$$
F(x,y)=c(x)c(y)sum^{N-1}_{i=0}{sum^{N-1}_{j=0}{f(i,j)cos(\frac {(i+0.5)π}{N}x)cos(\frac {(j+0.5)π}{N}y)}}
$$

$$
c(x)=\left\{\begin{matrix}\sqrt{\frac{1}{N}} ,x=0\\\sqrt{\frac{2}{N}} ,x!=0 \end{matrix}\right.
$$

二维DCT变换也可表示为：

$$
F=AfA^T
$$

$$
A(i,j)=c(i)cos(\frac {(j+0.5)π}{N}i)
$$

此形式更方便计算。DCT变换是对称的，因此可以对经过DCT变换的图片进行还原操作。

Examples
-------

计算图像感知相似度时，首先计算图像的PHASH值，再采用海明（hamming）距离相似度计算图片PHASH值的相似度。
```
#采用感知hash计算图片的感知相似度
import os
from scient.image import hash
from scient.algorithms import similar
import numpy
from PIL import Image

ref_image='test/data/I10.BMP'
images=['test/data/I10.BMP','test/data/i10_23_3.bmp','test/data/i10_23_4.bmp','test/data/i10_23_5.bmp','test/data/i10_24_5.bmp']

#读取图像文件
ref_image=Image.open(os.path.join(os.path.dirname(hash.__file__),'..',ref_image))
images=[Image.open(os.path.join(os.path.dirname(hash.__file__),'..',i)) for i in images]

#计算感知hash
phash=hash.percept(numpy.array(ref_image.convert("L")))
phashs=[hash.percept(numpy.array(i.convert("L"))) for i in images]

#计算感知相似度
for i in phashs:
    print(similar.hamming(i,phash))
```

运行结果

```
1.0
0.9384615384615385
0.8615384615384616
0.8153846153846154
0.6
```

## scient.neuralnet

神经网络相关算法模块，包括attention、transformer、bert、lstm、resnet、crf、dataset、fit等。

### scient.neuralnet.fit

神经网络训练模块，将torch构建的神经网络模型的训练方式简化为model.fit()，使torch神经网络模型训练更简捷，更优雅。

使用步骤：

（1）基于torch构建模型model，采用torch.utils.data.DataLoader加载训练数据集train_loader、验证数据集eval_loader(可选)；

（2）采用fit.set()设置模型训练参数，参数详情：
* optimizer=None: 优化器，可以用类似torch.optim模块内的优化器来定义；
* scheduler=None: 优化器的调度器，可以用类似torch.optim.lr_scheduler模块内的调度器来定义；
* loss_func=None: 损失函数，可以用类似torch.nn.CrossEntropyLoss()来定义；
* grad_func=None: 梯度操作函数，可进行如梯度裁剪的操作；
* perform_func=None: 模型性能函数，模型传入预测值和实际值，用以评估模型性能；
* n_iter=10: 模型在数据集上迭代训练的次数；
    - 如果n_iter为int,表示模型在数据集上迭代训练n_iter后停止；
    - 如果n_iter为(int,int),表示模型在数据集上迭代训练的最小min_iter和最大max_iter次数, 如果迭代次数超过min_iter且eval的perform_func比上一个iter大，结束训练。n_iter为(int,int)时，必须提供eval_loader，且perform_func必须是一个数值，且值越大模型性能越好；
* device=None: 模型训练的设备，如device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')；
* n_batch_step: 每n个batch更新一次optimizer的梯度，以节省显存及计算量；
* n_batch_plot: 每n个batch更新一下损失曲线，训练过程中会实时绘制损失曲线；
* save_path: 每个iter完成后模型保存路径，模型名为“模型类名_iter_i.checkpoint”,保存的内容为{'model_state_dict':model.state_dict(),'optimizer_state_dict':optimizer.state_dict(),'batch_loss':batch_loss}，如果训练时未提供eval_loader，batch_loss=train_batch_loss, 否则batch_loss=[train_batch_loss,eval_batch_loss]

（3）采用model.fit(train_loader,eval_loader,mode=('input','target'))训练模型：
* train_loader: 训练数据集
* eval_loader: 验证数据集
* mode: 数据集包含的内容，分四种情况：
    - mode=('input','target'), loader data item is one input and one target;
    - mode='input', loader data item is only one input;
    - mode=('inputs','target'), loader data item is a list of input and one target;
    - mode='inputs', loader data item is a list of input.
    - mode中不包含target时，不能使用perform_func
        
Examples
-------

首先构建模型model、训练数据加载器train_loader、验证数据加载器eval_loader：

```
import os
import torch
from scient.neuralnet import resnet, fit
import torchvision.transforms as tt
from torchvision.datasets import ImageFolder

# 数据转换（归一化和数据增强）
stats = ((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010))
train_tfms = tt.Compose([tt.RandomCrop(160, padding=4, padding_mode='reflect'), 
                         tt.RandomHorizontalFlip(), 
                         tt.ToTensor(), 
                         tt.Normalize(*stats,inplace=True)])
valid_tfms = tt.Compose([tt.Resize([160,160]),tt.ToTensor(), tt.Normalize(*stats)])

# 创建ImageFolder对象
data_train = ImageFolder(os.path.join(os.path.dirname(fit.__file__),'..','test/data/imagewoof/train'), train_tfms)
data_eval = ImageFolder(os.path.join(os.path.dirname(fit.__file__),'..','test/data/imagewoof/val'), valid_tfms)

# 设置批量大小
batch_size = 2

# 创建训练集和验证集的数据加载器
train_loader = torch.utils.data.DataLoader(data_train, batch_size=batch_size, shuffle=True)
eval_loader = torch.utils.data.DataLoader(data_eval, batch_size=batch_size, shuffle=False)

#resnet50模型
model=resnet.ResNet50(n_class=3)
```

然后设置模型训练参数、训练模型：

```
#设置训练参数
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
optimizer = torch.optim.Adam(model.parameters(), lr=0.0001, weight_decay=1e-4)
loss_func=torch.nn.CrossEntropyLoss()
model=fit.set(model,optimizer=optimizer,loss_func=loss_func,n_iter=5,device=device)

#训练
model.fit(train_loader=train_loader,eval_loader=eval_loader,mode=('input','target'))
```

运行结果：

```
train iter 0: avg_batch_loss=1.27345: 100%|██████████| 60/60 [00:04<00:00, 12.92it/s]                   
eval iter 0: avg_batch_loss=1.33363: 100%|██████████| 8/8 [00:00<00:00, 59.44it/s]                   
train iter 1: avg_batch_loss=1.24023: 100%|██████████| 60/60 [00:04<00:00, 13.39it/s]                   
eval iter 1: avg_batch_loss=1.08319: 100%|██████████| 8/8 [00:00<00:00, 58.83it/s]                   
train iter 2: batch_loss=1.42699 avg_batch_loss=1.16666:  63%|██████▎   | 38/60 [00:02<00:01, 13.37it/s]
```

Examples: 训练时不使用eval_loader
-------

```
#设置训练参数
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
optimizer = torch.optim.Adam(model.parameters(), lr=0.0001, weight_decay=1e-4)
loss_func=torch.nn.CrossEntropyLoss()
model=fit.set(model,optimizer=optimizer,loss_func=loss_func,n_iter=5,device=device)

#训练
model.fit(train_loader=train_loader,mode=('input','target'))
```

运行结果：

```
train iter 0: avg_batch_loss=1.07998: 100%|██████████| 60/60 [00:04<00:00, 12.27it/s]                   
train iter 1: avg_batch_loss=1.16323: 100%|██████████| 60/60 [00:04<00:00, 12.95it/s]                   
train iter 2: batch_loss=0.61398 avg_batch_loss=1.00838:  67%|██████▋   | 40/60 [00:03<00:01, 13.06it/s]
```

Examples: 使用scheduler在训练过程中改变学习率等optimizer参数
-------

```
#设置训练参数
n_iter=5
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
optimizer = torch.optim.Adam(model.parameters(), lr=0.0001, weight_decay=1e-4)
scheduler = torch.optim.lr_scheduler.OneCycleLR(optimizer, max_lr=0.0001, epochs=n_iter,steps_per_epoch=len(train_loader))
loss_func=torch.nn.CrossEntropyLoss()
model=fit.set(model,optimizer=optimizer,loss_func=loss_func,n_iter=n_iter,device=device)

#训练
model.fit(train_loader=train_loader,eval_loader=eval_loader,mode=('input','target'))
```

Examples: 使用perform_func在训练过程中评估模型性能
-------

```
#设置训练参数
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
optimizer = torch.optim.Adam(model.parameters(), lr=0.0001, weight_decay=1e-4)
loss_func=torch.nn.CrossEntropyLoss()
def perform_func(y_hat,y):#perform_func的输入是预测值y_hat和实际值y
    y_hat,y=torch.concat(y_hat),torch.concat(y)#先将y_hat和y分别concat，由于y_hat和y是按loader分批计算和收集的，所以y_hat和y是batch_size大小的多个对象组成的list
    _,y_hat=y_hat.max(axis=1)#该模型输出值y_hat最大值对应的索引是预测的类别
    return round((y_hat==y).sum().item()/len(y),4)#输出准确率，并保留4位小数
model=fit.set(model,optimizer=optimizer,loss_func=loss_func,perform_func=perform_func,n_iter=5,device=device)

#训练
model.fit(train_loader=train_loader,eval_loader=eval_loader,mode=('input','target'))
```

运行结果，可以在每个iter结束后得到perform的值：

```
train iter 0: avg_batch_loss=1.27428 perform=0.3417: 100%|██████████| 60/60 [00:04<00:00, 12.34it/s]    
eval iter 0: avg_batch_loss=1.09305 perform=0.4: 100%|██████████| 8/8 [00:00<00:00, 55.59it/s]       
train iter 1: avg_batch_loss=1.09102 perform=0.4417: 100%|██████████| 60/60 [00:04<00:00, 13.30it/s]    
eval iter 1: avg_batch_loss=1.18128 perform=0.4: 100%|██████████| 8/8 [00:00<00:00, 60.46it/s]       
train iter 2: avg_batch_loss=1.24860 perform=0.3583: 100%|██████████| 60/60 [00:04<00:00, 13.19it/s]    
eval iter 2: avg_batch_loss=1.23469 perform=0.4: 100%|██████████| 8/8 [00:00<00:00, 60.57it/s]       
```

Examples: 使用grad_func在训练过程对梯度进行裁剪
-------

```
#设置训练参数
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
optimizer = torch.optim.Adam(model.parameters(), lr=0.0001, weight_decay=1e-4)
loss_func=torch.nn.CrossEntropyLoss()
def grad_func(x):#grad_func的输入是model.parameters(),该操作在loss.backward()后起作用
    torch.nn.utils.clip_grad_value_(x, 0.1)
model=fit.set(model,optimizer=optimizer,loss_func=loss_func,grad_func=grad_func,n_iter=5,device=device)

#训练
model.fit(train_loader=train_loader,eval_loader=eval_loader,mode=('input','target'))
```

Examples: 使用n_batch_step在小显存上模拟大batch_size的训练
-------
该功能实现了多次反向误差传播并累积梯度后，再让optimizer进行梯度下降优化。

```
#设置训练参数
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
optimizer = torch.optim.Adam(model.parameters(), lr=0.0001, weight_decay=1e-4)
loss_func=torch.nn.CrossEntropyLoss()
model=fit.set(model,optimizer=optimizer,loss_func=loss_func,n_iter=5,device=device,n_batch_step=5)

#训练
model.fit(train_loader=train_loader,eval_loader=eval_loader,mode=('input','target'))
```

Examples: 当训练到一定迭代次数后，如果模型在验证集上性能下降，提前停止训练
-------

用n_iter=(min_iter,max_iter)设置模型的最小和最大训练迭代次数，当模型训练迭次数超过min_iter时，判断本次迭代训练模型性能是否优于上次迭代训练模型性能，如果不优于上次，则停止训练。过功能可防止过多的训练导致过拟合。该功能需要在eval_loader上计算perform，因此eval_loader不能为空，且perform_func输出必须为一个数值，该数值越大表示模型越优。

```
#设置训练参数
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
optimizer = torch.optim.Adam(model.parameters(), lr=0.0001, weight_decay=1e-4)
loss_func=torch.nn.CrossEntropyLoss()
def perform_func(y_hat,y):#perform_func的输入是预测值y_hat和实际值y
    y_hat,y=torch.concat(y_hat),torch.concat(y)#先将y_hat和y分别concat，由于y_hat和y是按loader分批计算和收集的，所以y_hat和y是batch_size大小的多个对象组成的list
    _,y_hat=y_hat.max(axis=1)#该模型输出值y_hat最大值对应的索引是预测的类别
    return round((y_hat==y).sum().item()/len(y),4)#输出准确率，并保留4位小数
model=fit.set(model,optimizer=optimizer,loss_func=loss_func,perform_func=perform_func,n_iter=(5,20),device=device)

#训练
model.fit(train_loader=train_loader,eval_loader=eval_loader,mode=('input','target'))
```

运行结果，可以看到模型运行到第iter 6停止，并提示性能最佳的模型是iter 4：

```
train iter 0: avg_batch_loss=1.17016 perform=0.375: 100%|██████████| 60/60 [00:04<00:00, 12.60it/s]     
eval iter 0: avg_batch_loss=1.48805 perform=0.3333: 100%|██████████| 8/8 [00:00<00:00, 60.23it/s]    
train iter 1: avg_batch_loss=1.17200 perform=0.3833: 100%|██████████| 60/60 [00:04<00:00, 13.08it/s]    
eval iter 1: avg_batch_loss=1.18933 perform=0.2667: 100%|██████████| 8/8 [00:00<00:00, 59.39it/s]    
train iter 2: avg_batch_loss=1.09923 perform=0.4333: 100%|██████████| 60/60 [00:04<00:00, 13.14it/s]    
eval iter 2: avg_batch_loss=1.32449 perform=0.3333: 100%|██████████| 8/8 [00:00<00:00, 60.92it/s]    
train iter 3: avg_batch_loss=1.20507 perform=0.4083: 100%|██████████| 60/60 [00:05<00:00, 11.66it/s]    
eval iter 3: avg_batch_loss=1.23331 perform=0.2667: 100%|██████████| 8/8 [00:00<00:00, 57.59it/s]    
train iter 4: avg_batch_loss=1.09205 perform=0.4167: 100%|██████████| 60/60 [00:04<00:00, 12.87it/s]    
eval iter 4: avg_batch_loss=1.11206 perform=0.4: 100%|██████████| 8/8 [00:00<00:00, 59.80it/s]       
train iter 5: avg_batch_loss=1.10706 perform=0.4583: 100%|██████████| 60/60 [00:04<00:00, 12.94it/s]    
eval iter 5: avg_batch_loss=1.07162 perform=0.4: 100%|██████████| 8/8 [00:00<00:00, 39.96it/s]       
train iter 6: avg_batch_loss=1.15846 perform=0.4333: 100%|██████████| 60/60 [00:04<00:00, 12.34it/s]    
eval iter 6: avg_batch_loss=1.16467 perform=0.4: 100%|██████████| 8/8 [00:00<00:00, 58.85it/s]early stop and the best model is iter 4, the perform is 0.4
```

Examples: 训练过程中实时显示loss曲线，并在每一个iter完成后保存模型
-------

设置n_batch_plot和save_path，保存的模型以checkpoint为后缀名，可以用torch.load打开保存的模型，模型里保存了3项内容：model_state_dict、optimizer_state_dict、batch_loss

```
#设置训练参数
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
optimizer = torch.optim.Adam(model.parameters(), lr=0.0001, weight_decay=1e-4)
loss_func=torch.nn.CrossEntropyLoss()
model=fit.set(model,optimizer=optimizer,loss_func=loss_func,n_iter=5,device=device,n_batch_plot=5,save_path='d:/')

#训练
model.fit(train_loader=train_loader,eval_loader=eval_loader,mode=('input','target'))

#打开并查看保存的模型
checkpoint=torch.load('D:/ResNet_iter_2.checkpoint')
checkpoint.keys()
checkpoint['batch_loss']
checkpoint['model_state_dict']
```

Examples: 如果型输出结果本身就是损失，可以省略loss_func
-------
先定义一个输出为loss的模型

```
#模型
class output_loss(torch.nn.Module):
    def __init__(self):
        super(output_loss,self).__init__()

        self.model=resnet.ResNet50(n_class=3)
        self.loss_func=torch.nn.CrossEntropyLoss()

    def forward(self,x,y):
        y_hat=self.model(x)
        return self.loss_func(y_hat,y)#输出为loss无需在训练过程中计算loss
    
model=output_loss()
```

然后设置模型训练参数时，省略loss_func，因为此时loader的input和target都要输入到模型的forward中，因此可以将其看成inputs=[input,target]，在训练时mode='inputs'

```
#设置训练参数
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
optimizer = torch.optim.Adam(model.parameters(), lr=0.0001, weight_decay=1e-4)
model=fit.set(model,optimizer=optimizer,n_iter=10,device=device)

#训练
model.fit(train_loader=train_loader,eval_loader=eval_loader,mode='inputs')
```

Examples: 如果型输出结果有多个值，只用其中的1个值计算损失，需要自定义loss_func
-------
先定义一个输出为多个值的模型

```
#模型
class output_multi(torch.nn.Module):
    def __init__(self):
        super(output_multi,self).__init__()

        self.model=resnet.ResNet50(n_class=3)

    def forward(self,x):
        y_hat=self.model(x)
        return y_hat,x#输出为两个值，只使用y_hat计算损失

model=output_multi()
```

然后设置模型训练参数时，对loss_func进行修改，用其中需要参与loss计算的部分计算loss

```
loss_func_=torch.nn.CrossEntropyLoss()
def loss_func(y_hat,y):
    return loss_func_(y_hat[0],y)#指定用输型输出的第0个值计算loss

#设置训练参数
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
optimizer = torch.optim.Adam(model.parameters(), lr=0.0001, weight_decay=1e-4)
model=fit.set(model,optimizer=optimizer,loss_func=loss_func,n_iter=10,device=device)

#训练
model.fit(train_loader=train_loader,eval_loader=eval_loader,mode=('input','target'))
```

