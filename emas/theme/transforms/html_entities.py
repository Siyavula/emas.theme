# encoding: utf-8
x = """
Greek capital letter alpha 	&Alpha; 	&#913; 	&#x391; 	Α 	Α 	Α
Greek capital letter beta 	&Beta; 	&#914; 	&#x392; 	Β 	Β 	Β
Greek capital letter gamma 	&Gamma; 	&#915; 	&#x393; 	Γ 	Γ 	Γ
Greek capital letter delta 	&Delta; 	&#916; 	&#x394; 	Δ 	Δ 	Δ
Greek capital letter epsilon 	&Epsilon; 	&#917; 	&#x395; 	Ε 	Ε 	Ε
Greek capital letter zeta 	&Zeta; 	&#918; 	&#x396; 	Ζ 	Ζ 	Ζ
Greek capital letter eta 	&Eta; 	&#919; 	&#x397; 	Η 	Η 	Η
Greek capital letter theta 	&Theta; 	&#920; 	&#x398; 	Θ 	Θ 	Θ
Greek capital letter iota 	&Iota; 	&#921; 	&#x399; 	Ι 	Ι 	Ι
Greek capital letter kappa 	&Kappa; 	&#922; 	&#x39A; 	Κ 	Κ 	Κ
Greek capital letter lambda 	&Lambda; 	&#923; 	&#x39B; 	Λ 	Λ 	Λ
Greek capital letter mu 	&Mu; 	&#924; 	&#x39C; 	Μ 	Μ 	Μ
Greek capital letter nu 	&Nu; 	&#925; 	&#x39D; 	Ν 	Ν 	Ν
Greek capital letter xi 	&Xi; 	&#926; 	&#x39E; 	Ξ 	Ξ 	Ξ
Greek capital letter omicron 	&Omicron; 	&#927; 	&#x39F; 	Ο 	Ο 	Ο
Greek capital letter pi 	&Pi; 	&#928; 	&#x3A0; 	Π 	Π 	Π
Greek capital letter rho 	&Rho; 	&#929; 	&#x3A1; 	Ρ 	Ρ 	Ρ
Greek capital letter sigma 	&Sigma; 	&#931; 	&#x3A3; 	Σ 	Σ 	Σ
Greek capital letter tau 	&Tau; 	&#932; 	&#x3A4; 	Τ 	Τ 	Τ
Greek capital letter upsilon 	&Upsilon; 	&#933; 	&#x3A5; 	Υ 	Υ 	Υ
Greek capital letter phi 	&Phi; 	&#934; 	&#x3A6; 	Φ 	Φ 	Φ
Greek capital letter chi 	&Chi; 	&#935; 	&#x3A7; 	Χ 	Χ 	Χ
Greek capital letter psi 	&Psi; 	&#936; 	&#x3A8; 	Ψ 	Ψ 	Ψ
Greek capital letter omega 	&Omega; 	&#937; 	&#x3A9; 	Ω 	Ω 	Ω
Greek small letter alpha 	&alpha; 	&#945; 	&#x3B1; 	α 	α 	α
Greek small letter beta 	&beta; 	&#946; 	&#x3B2; 	β 	β 	β
Greek small letter gamma 	&gamma; 	&#947; 	&#x3B3; 	γ 	γ 	γ
Greek small letter delta 	&delta; 	&#948; 	&#x3B4; 	δ 	δ 	δ
Greek small letter epsilon 	&epsilon; 	&#949; 	&#x3B5; 	ε 	ε 	ε
Greek small letter lunate epsilon 	&straightepsilon; 	&#1013; 	&#x3F5;
Greek small letter zeta 	&zeta; 	&#950; 	&#x3B6; 	ζ 	ζ 	ζ
Greek small letter eta 	&eta; 	&#951; 	&#x3B7; 	η 	η 	η
Greek small letter theta 	&theta; 	&#952; 	&#x3B8; 	θ 	θ 	θ
Greek small letter iota 	&iota; 	&#953; 	&#x3B9; 	ι 	ι 	ι
Greek small letter kappa 	&kappa; 	&#954; 	&#x3BA; 	κ 	κ 	κ
Greek small letter lambda 	&lambda; 	&#955; 	&#x3BB; 	λ 	λ 	λ
Greek small letter mu 	&mu; 	&#956; 	&#x3BC; 	μ 	μ 	μ
Greek small letter nu 	&nu; 	&#957; 	&#x3BD; 	ν 	ν 	ν
Greek small letter xi 	&xi; 	&#958; 	&#x3BE; 	ξ 	ξ 	ξ
Greek small letter omicron 	&omicron; 	&#959; 	&#x3BF; 	ο 	ο 	ο
Greek small letter pi 	&pi; 	&#960; 	&#x3C0; 	π 	π 	π
Greek small letter rho 	&rho; 	&#961; 	&#x3C1; 	ρ 	ρ 	ρ
Greek small letter final sigma 	&sigmaf; 	&#962; 	&#x3C2; 	ς 	ς 	ς
Greek small letter sigma 	&sigma; 	&#963; 	&#x3C3; 	σ 	σ 	σ
Greek small letter tau 	&tau; 	&#964; 	&#x3C4; 	τ 	τ 	τ
Greek small letter upsilon 	&upsilon; 	&#965; 	&#x3C5; 	υ 	υ 	υ
Greek small letter phi 	&phi; 	&#966; 	&#x3C6; 	φ 	φ 	φ
Greek small letter chi 	&chi; 	&#967; 	&#x3C7; 	χ 	χ 	χ
Greek small letter psi 	&psi; 	&#968; 	&#x3C8; 	ψ 	ψ 	ψ
Greek small letter omega 	&omega; 	&#969; 	&#x3C9; 	ω 	ω 	ω
Greek small letter theta symbol 	&thetasym; 	&#977; 	&#x3D1; 	ϑ 	ϑ 	ϑ
Greek upsilon with hook symbol 	&upsih; 	&#978; 	&#x3D2; 	ϒ 	ϒ 	ϒ
Greek pi symbol 	&piv; 	&#982; 	&#x3D6; 	ϖ 	ϖ 	ϖ
bullet = black small circle 	&bull; 	&#8226; 	&#x2022; 	• 	• 	•
horizontal ellipsis = three dot leader 	&hellip; 	&#8230; 	&#x2026; 	… 	… 	…
prime = minutes = feet 	&prime; 	&#8242; 	&#x2032; 	′ 	′ 	′
double prime = seconds = inches 	&Prime; 	&#8243; 	&#x2033; 	″ 	″ 	″
overline = spacing overscore 	&oline; 	&#8254; 	&#x203E; 	‾ 	‾ 	‾
fraction slash 	&frasl; 	&#8260; 	&#x2044; 	⁄ 	⁄ 	⁄
script capital P = power set = Weierstrass p 	&weierp; 	&#8472; 	&#x2118; 	℘ 	℘ 	℘
blackletter capital I = imaginary part 	&image; 	&#8465; 	&#x2111; 	ℑ 	ℑ 	ℑ
blackletter capital R = real part symbol 	&real; 	&#8476; 	&#x211C; 	ℜ 	ℜ 	ℜ
trade mark sign 	&trade; 	&#8482; 	&#x2122; 	™ 	™ 	™
alef symbol = first transfinite cardinal 	&alefsym; 	&#8501; 	&#x2135; 	ℵ 	ℵ 	ℵ
leftwards arrow 	&larr; 	&#8592; 	&#x2190; 	← 	← 	←
upwards arrow 	&uarr; 	&#8593; 	&#x2191; 	↑ 	↑ 	↑
rightwards arrow 	&rarr; 	&#8594; 	&#x2192; 	→ 	→ 	→
downwards arrow 	&darr; 	&#8595; 	&#x2193; 	↓ 	↓ 	↓
left right arrow 	&harr; 	&#8596; 	&#x2194; 	↔ 	↔ 	↔
downwards arrow with corner leftwards = carriage return 	&crarr; 	&#8629; 	&#x21B5; 	↵ 	↵ 	↵
leftwards double arrow 	&lArr; 	&#8656; 	&#x21D0; 	⇐ 	⇐ 	⇐
upwards double arrow 	&uArr; 	&#8657; 	&#x21D1; 	⇑ 	⇑ 	⇑
rightwards double arrow 	&rArr; 	&#8658; 	&#x21D2; 	⇒ 	⇒ 	⇒
downwards double arrow 	&dArr; 	&#8659; 	&#x21D3; 	⇓ 	⇓ 	⇓
left right double arrow 	&hArr; 	&#8660; 	&#x21D4; 	⇔ 	⇔ 	⇔
for all 	&forall; 	&#8704; 	&#x2200; 	∀ 	∀ 	∀
partial differential 	&part; 	&#8706; 	&#x2202; 	∂ 	∂ 	∂
there exists 	&exist; 	&#8707; 	&#x2203; 	∃ 	∃ 	∃
empty set = null set = diameter 	&empty; 	&#8709; 	&#x2205; 	∅ 	∅ 	∅
nabla = backward difference 	&nabla; 	&#8711; 	&#x2207; 	∇ 	∇ 	∇
element of 	&isin; 	&#8712; 	&#x2208; 	∈ 	∈ 	∈
not an element of 	&notin; 	&#8713; 	&#x2209; 	∉ 	∉ 	∉
contains as member 	&ni; 	&#8715; 	&#x220B; 	∋ 	∋ 	∋
n-ary product = product sign 	&prod; 	&#8719; 	&#x220F; 	∏ 	∏ 	∏
n-ary sumation 	&sum; 	&#8721; 	&#x2211; 	∑ 	∑ 	∑
minus sign 	&minus; 	&#8722; 	&#x2212; 	− 	− 	−
asterisk operator 	&lowast; 	&#8727; 	&#x2217; 	∗ 	∗ 	∗
square root = radical sign 	&radic; 	&#8730; 	&#x221A; 	√ 	√ 	√
proportional to 	&prop; 	&#8733; 	&#x221D; 	∝ 	∝ 	∝
proportional to 	&propto; 	&#8733; 	&#x221D; 	∝ 	∝ 	∝
infinity 	&infin; 	&#8734; 	&#x221E; 	∞ 	∞ 	∞
angle 	&ang; 	&#8736; 	&#x2220; 	∠ 	∠ 	∠
logical and = wedge 	&and; 	&#8743; 	&#x2227; 	∧ 	∧ 	∧
logical or = vee 	&or; 	&#8744; 	&#x2228; 	∨ 	∨ 	∨
intersection = cap 	&cap; 	&#8745; 	&#x2229; 	∩ 	∩ 	∩
union = cup 	&cup; 	&#8746; 	&#x222A; 	∪ 	∪ 	∪
integral 	&int; 	&#8747; 	&#x222B; 	∫ 	∫ 	∫
therefore 	&there4; 	&#8756; 	&#x2234; 	∴ 	∴ 	∴
tilde operator = varies with = similar to 	&sim; 	&#8764; 	&#x223C; 	∼ 	∼ 	∼
approximately equal to 	&cong; 	&#8773; 	&#x2245; 	≅ 	≅ 	≅
almost equal to = asymptotic to 	&asymp; 	&#8776; 	&#x2248; 	≈ 	≈ 	≈
not equal to 	&ne; 	&#8800; 	&#x2260; 	≠ 	≠ 	≠
identical to 	&equiv; 	&#8801; 	&#x2261; 	≡ 	≡ 	≡
less-than or equal to 	&le; 	&#8804; 	&#x2264; 	≤ 	≤ 	≤
greater-than or equal to 	&ge; 	&#8805; 	&#x2265; 	≥ 	≥ 	≥
subset of 	&sub; 	&#8834; 	&#x2282; 	⊂ 	⊂ 	⊂
superset of 	&sup; 	&#8835; 	&#x2283; 	⊃ 	⊃ 	⊃
not a subset of 	&nsub; 	&#8836; 	&#x2284; 	⊄ 	⊄ 	⊄
subset of or equal to 	&sube; 	&#8838; 	&#x2286; 	⊆ 	⊆ 	⊆
superset of or equal to 	&supe; 	&#8839; 	&#x2287; 	⊇ 	⊇ 	⊇
circled plus = direct sum 	&oplus; 	&#8853; 	&#x2295; 	⊕ 	⊕ 	⊕
circled times = vector product 	&otimes; 	&#8855; 	&#x2297; 	⊗ 	⊗ 	⊗
up tack = orthogonal to = perpendicular 	&perp; 	&#8869; 	&#x22A5; 	⊥ 	⊥ 	⊥
dot operator 	&sdot; 	&#8901; 	&#x22C5; 	⋅ 	⋅ 	⋅
left ceiling = APL upstile 	&lceil; 	&#8968; 	&#x2308; 	⌈ 	⌈ 	⌈
right ceiling 	&rceil; 	&#8969; 	&#x2309; 	⌉ 	⌉ 	⌉
left floor = APL downstile 	&lfloor; 	&#8970; 	&#x230A; 	⌊ 	⌊ 	⌊
right floor 	&rfloor; 	&#8971; 	&#x230B; 	⌋ 	⌋ 	⌋
left-pointing angle bracket = bra 	&lang; 	&#9001; 	&#x2329; 	〈 	〈 	〈
right-pointing angle bracket = ket 	&rang; 	&#9002; 	&#x232A; 	〉 	〉 	〉
lozenge 	&loz; 	&#9674; 	&#x25CA; 	◊ 	◊ 	◊
black spade suit 	&spades; 	&#9824; 	&#x2660; 	♠ 	♠ 	♠
black club suit = shamrock 	&clubs; 	&#9827; 	&#x2663; 	♣ 	♣ 	♣
black heart suit = valentine 	&hearts; 	&#9829; 	&#x2665; 	♥ 	♥ 	♥
black diamond suit 	&diams; 	&#9830; 	&#x2666; 	♦ 	♦ 	♦
script small l 	&ell; 	&#8467; 	&#x2113; 	ℓ
rightwards arrow 	&rightarrow; 	&#8594; 	&#x2192; 	→ 	→ 	→
leftwards arrow 	&leftarrow; 	&#8592; 	&#x2190; 	← 	← 	←
middle dot 	&middot; 	&#183;	&#xB7; 	· 	· 	·
therefore 	&therefore; 	&#8756; 	&#x2234; 	∴ 	∴ 	∴
almost equal to = asymptotic to 	&approx; 	&#8776; 	&#x2248; 	≈ 	≈ 	≈
multiplication sign 	&times; 	&#215;	&#xD7; 	× 	× 	×
division sign 	&div; 	&#247;	&#xF7;	÷	÷	÷
division sign 	&divide; 	&#247;	&#xF7;	÷	÷	÷
triangle 	&triangle; 	&#9651;	&#x25B3;
square 	&square; 	&#9633;	&#x25A1;
small unfilled circle 	&SmallCircle; 	&#2218;
Greek small letter final sigma 	&sigmav; 	&#962; 	&#x3C2; 	ς 	ς 	ς
n-dash 	&ndash; 	&#8211;
m-dash 	&mdash; 	&#8212;
Greek tonos diacritical mark 	&acute; 	&#900; 	&#x384; 	ς 	ς 	ς
MathML: double-struck capital N	&Nopf; 	&#8469; 	&#x2115; 	ℕ
MathML: double-struck capital Q	&Qopf; 	&#8474; 	&#x211A; 	ℚ
MathML: double-struck capital R	&Ropf; 	&#8477; 	&#x211D; 	
MathML: double-struck capital Z	&Zopf; 	&#8484; 	&#x2124; 	ℤ
MathML: left curly bracket	&lbrace; 	&#123; 	&#x7B; 	{
MathML: right curly bracket	&rbrace; 	&#125; 	&#x7D; 	}
MathML: dot above	&dot; 	&#729; 	&#x2D9; 	
MathML: macron	&OverBar; 	&#175; 	&#xAF; 	
MathML: plus-minus sign	&pm; 	&#177; 	&#xB1; 	±
MathML: element of	&Element; 	&#8712; 	&#x2208; 	∈
MathML: midline horizontal ellipsis	&ctdot; 	&#8943; 	&#x22EF; 	⋯
MathML: vertical ellipsis	&vellip; 	&#8942; 	&#x22EE; 	⋮
MathML: circumflex accent	&Hat; 	&#94; 	&#x5E; 	^
MathML: parallel to	&parallel; 	&#8741; 	&#x2225; 	∥
MathML: bullet	&bullet; 	&#8226; 	&#x2022; 	•
MathML: leftwards harpoon over rightwards harpoon	&rightleftharpoons; 	&#8651; 	&#x21CB;
MathML: presentation form for vertical right curly bracket	&UnderBrace; 	&#65080; 	&#xFE38;
""".strip().split('\n')

mapping = {}
for line in x:
    y = line.split('\t')
    mapping[y[1].strip()] = y[2].strip()
