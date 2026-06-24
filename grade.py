from PIL import Image, ImageOps, ImageEnhance, ImageFilter, ImageDraw
import math, random
random.seed(7)

src = Image.open(r'img/ringov_src.png').convert('RGB')
W,H = src.size  # 770x513

# 1) Crop to emphasise the two foreground players + keep some motion of the runner
# keep left 0..0.80 width, full height, slight top trim
crop = src.crop((0, 12, int(W*0.82), H))
cw,ch = crop.size

# 2) upscale ~2.6x with high quality
scale = 2.7
big = crop.resize((int(cw*scale), int(ch*scale)), Image.LANCZOS)
big = big.filter(ImageFilter.UnsharpMask(radius=2.2, percent=90, threshold=2))

# 3) to luminance, auto-contrast with slight clip + gentle S curve
g = ImageOps.grayscale(big)
g = ImageOps.autocontrast(g, cutoff=1)
# S-curve
lut=[]
for i in range(256):
    x=i/255.0
    y = x*x*(3-2*x)            # smoothstep -> punchy mids
    y = 0.10 + 0.86*y          # lift blacks a touch (print never pure black), pull highlights
    lut.append(max(0,min(255,int(y*255))))
g = g.point(lut)

# 4) Warm tritone (80s sports-mag print) duotone LUT
stops = [(0.00,(34,12,16)),(0.22,(86,28,26)),(0.46,(150,74,48)),
         (0.70,(206,150,104)),(1.00,(243,231,208))]
def ramp(t):
    for i in range(len(stops)-1):
        a,ca=stops[i]; b,cb=stops[i+1]
        if a<=t<=b:
            f=(t-a)/(b-a)
            return tuple(int(ca[k]+(cb[k]-ca[k])*f) for k in range(3))
    return stops[-1][1]
rL=[ramp(i/255.0)[0] for i in range(256)]
gL=[ramp(i/255.0)[1] for i in range(256)]
bL=[ramp(i/255.0)[2] for i in range(256)]
duo = Image.merge('RGB',(g.point(rL), g.point(gL), g.point(bL)))

# 5) subtle halftone dot overlay (CMYK print feel)
bw,bh = duo.size
ht = Image.new('L',(bw,bh),0)
hd = ImageDraw.Draw(ht)
step=4
for y in range(0,bh,step):
    for x in range(0,bw,step):
        # dot size modulated by local darkness
        lx = g.getpixel((min(bw-1,x),min(bh-1,y)))
        r = (1-lx/255.0)*1.7
        if r>0.3:
            hd.ellipse((x-r,y-r,x+r,y+r), fill=40)
ht = ht.filter(ImageFilter.GaussianBlur(0.4))
duo = Image.composite(Image.new('RGB',(bw,bh),(20,8,10)), duo, ht.point(lambda v:int(v*0.18)))

# 6) film grain
noise = Image.effect_noise((bw,bh), 16).convert('L')
noise = noise.point(lambda v:int((v-128)*0.5+128))
duo = Image.blend(duo, Image.merge('RGB',(noise,noise,noise)), 0.07)

# 7) warm overall + tiny saturation, vignette
duo = ImageEnhance.Color(duo).enhance(1.06)
duo = ImageEnhance.Contrast(duo).enhance(1.04)
# vignette
vig = Image.new('L',(bw,bh),0); vd=ImageDraw.Draw(vig)
vd.ellipse((-bw*0.18,-bh*0.18,bw*1.18,bh*1.18), fill=255)
vig = vig.filter(ImageFilter.GaussianBlur(bw*0.12))
dark = ImageEnhance.Brightness(duo).enhance(0.72)
duo = Image.composite(duo, dark, vig)

duo.save(r'img/ringov_graded.jpg', quality=92, dpi=(300,300))
duo.save(r'img/ringov_graded.png')
print('graded', duo.size, '-> ', round(duo.size[0]/300*25.4), 'x', round(duo.size[1]/300*25.4), 'mm @300dpi')
