# Restored-colour grade of the B&W source (no AI; positional + luminance tinting)
from PIL import Image, ImageOps, ImageEnhance, ImageFilter, ImageDraw, ImageChops
import math

src = Image.open(r'img/ringov_src.png').convert('RGB')
W,H = src.size                       # 770 x 513
# portrait-friendly crop centred on the two foreground players
crop = src.crop((40, 8, int(W*0.74), H))
cw,ch = crop.size
scale = 3.2
big = crop.resize((int(cw*scale), int(ch*scale)), Image.LANCZOS)
big = big.filter(ImageFilter.UnsharpMask(radius=2.0, percent=80, threshold=2))
bw,bh = big.size

# luminance, contrast
L = ImageOps.grayscale(big)
L = ImageOps.autocontrast(L, cutoff=1)
lut=[]
for i in range(256):
    x=i/255.0
    y=x*x*(3-2*x)
    y=0.06+0.90*y
    lut.append(max(0,min(255,int(y*255))))
L = L.point(lut)

# base "faded colour film": near-neutral warm (de-sepia, light)
base = ImageOps.colorize(L, black=(26,22,26), mid=(132,120,104), white=(246,242,231)).convert('RGB')

# gentle global warmth + low saturation lift
r,g,b = base.split()
r = r.point(lambda v:min(255,int(v*1.05)))
b = b.point(lambda v:int(v*0.96))
base = Image.merge('RGB',(r,g,b))

# --- GRASS: green tint in the lower band where tone is mid (pitch) ---
grad = Image.new('L',(bw,bh),0); gd=ImageDraw.Draw(grad)
for y in range(bh):
    t=(y/bh-0.70)/0.30          # ramps 0..1 over bottom 30%
    v=int(max(0,min(1,t))*255)
    gd.line([(0,y),(bw,y)], fill=v)
# only where luminance is mid (grass), not the dark shorts/socks
midmask = L.point(lambda v: 255 if 60<v<185 else 0).filter(ImageFilter.GaussianBlur(3))
grassmask = ImageChops.multiply(grad, midmask).point(lambda v:int(v*0.85))
green = Image.new('RGB',(bw,bh),(74,104,46))
base = Image.composite(Image.blend(base, green, 0.55), base, grassmask)

# --- subtle skin warmth in upper-mid highlights (faces/arms) ---
hi = L.point(lambda v: 255 if 150<v<210 else 0).filter(ImageFilter.GaussianBlur(2))
# limit to upper 55% (where players' upper bodies are)
topgrad = Image.new('L',(bw,bh),0); td=ImageDraw.Draw(topgrad)
for y in range(bh):
    v = 255 if y < bh*0.55 else max(0,int(255*(1-(y/bh-0.55)/0.2)))
    td.line([(0,y),(bw,y)], fill=v)
skinmask = ImageChops.multiply(hi, topgrad).point(lambda v:int(v*0.35))
skin = Image.new('RGB',(bw,bh),(214,164,128))
base = Image.composite(Image.blend(base, skin, 0.5), base, skinmask)

# overall saturation + contrast
base = ImageEnhance.Color(base).enhance(1.18)
base = ImageEnhance.Contrast(base).enhance(1.05)
base = ImageEnhance.Brightness(base).enhance(1.02)

# film grain (subtle — restored archival)
noise = Image.effect_noise((bw,bh), 14).convert('L')
noise = noise.point(lambda v:int((v-128)*0.45+128))
base = Image.blend(base, Image.merge('RGB',(noise,noise,noise)), 0.05)

# soft vignette
vig = Image.new('L',(bw,bh),0); vd=ImageDraw.Draw(vig)
vd.ellipse((-bw*0.22,-bh*0.18,bw*1.22,bh*1.18), fill=255)
vig = vig.filter(ImageFilter.GaussianBlur(bw*0.13))
dark = ImageEnhance.Brightness(base).enhance(0.78)
base = Image.composite(base, dark, vig)

base.save(r'img/ringov_color.jpg', quality=92, dpi=(300,300))
print('color', base.size)

# --- pull the two bottom story thumbnails from the reference comp ---
ref = Image.open(r'C:\Users\User\.claude\uploads\4923c7d6-37f5-4bf1-9cf1-9ef0d9759205\c2a9ea0e-2859.png').convert('RGB')
RW,RH = ref.size
print('ref', RW, RH)
boot = ref.crop((int(RW*0.055), int(RH*0.835), int(RW*0.255), int(RH*0.965)))
stad = ref.crop((int(RW*0.515), int(RH*0.835), int(RW*0.75), int(RH*0.965)))
boot.resize((boot.width*3, boot.height*3), Image.LANCZOS).save(r'img/thumb_boot.jpg', quality=90)
stad.resize((stad.width*3, stad.height*3), Image.LANCZOS).save(r'img/thumb_stadium.jpg', quality=90)
print('thumbs saved', boot.size, stad.size)
