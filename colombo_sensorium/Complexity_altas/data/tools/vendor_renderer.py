#!/usr/bin/env python3
"""Render the self-contained English Complexity Atlas from canonical JSON.

Vendored from the supplied English Atlas renderer; the export adapter makes
the small documented publication-policy changes in export_profiles.py.

Usage: python render_atlas.py atlas.json --output . --pdf --workers 4
       python render_atlas.py settings/SETTING_ID/SETTING_ID.json --output preview --pdf
"""
from __future__ import annotations
import argparse, hashlib, collections, concurrent.futures, copy, html, json, pathlib, re, subprocess, unicodedata, textwrap

TOPICS={'single_objective':'Single-objective optimization','bilevel':'Bilevel optimization','minimax':'Minimax optimization','saddle_point':'Saddle-point problems','variational_inequality':'Variational inequalities','matrix_computation':'Matrix computation','online_bandit':'Online learning and bandits'}
AXES={'task':'Task','model':'Admissible model','oracle':'Oracle interface','output':'Output','metric':'Loss or accuracy criterion','resource':'Resource accounting'}
STATUS={'optimal':'Optimal','logarithmic_gap':'Logarithmic gap','polynomial_gap':'Polynomial gap','other_quantified_gap':'Other quantified gap','missing_upper':'Upper bound missing','missing_lower':'Lower bound missing','missing_both':'Both bounds missing','joint_budget_unclosed':'Joint budget unresolved','infinite_complexity':'Infinite complexity','infeasible_task':'Infeasible task'}
PREAMBLE=r'''\documentclass[10pt,a4paper]{article}
\usepackage[margin=20mm,headheight=15pt,headsep=7mm,footskip=10mm]{geometry}
\usepackage{fontspec,amsmath,amssymb,mathtools,microtype}
\setmainfont{lmroman10-regular.otf}[BoldFont=lmroman10-bold.otf,ItalicFont=lmroman10-italic.otf,BoldItalicFont=lmroman10-bolditalic.otf]
\setsansfont{lmsans10-regular.otf}[BoldFont=lmsans10-bold.otf,ItalicFont=lmsans10-oblique.otf,BoldItalicFont=lmsans10-boldoblique.otf]
\setmonofont[Scale=.86]{lmmono10-regular.otf}[ItalicFont=lmmono10-italic.otf]
\usepackage{ragged2e}\usepackage{xcolor,booktabs,longtable,array,graphicx,enumitem,fancyhdr,needspace,titlesec,hyperref,xurl}
\definecolor{AtlasNavy}{HTML}{18334C}\definecolor{AtlasTeal}{HTML}{116D73}\definecolor{AtlasGray}{HTML}{52616D}
\hypersetup{colorlinks=true,linkcolor=AtlasTeal,urlcolor=AtlasTeal,pdfcreator={Complexity Atlas},unicode=true}
\urlstyle{same}\setlength{\parindent}{0pt}\setlength{\parskip}{4.8pt}\setlength{\emergencystretch}{3em}
\renewcommand{\baselinestretch}{1.08}\setcounter{secnumdepth}{0}\setlist{nosep,leftmargin=1.5em}
\titleformat{\section}{\Large\bfseries\sffamily\color{AtlasNavy}\raggedright}{}{0em}{}
\titleformat{\subsection}{\large\bfseries\sffamily\color{AtlasTeal}\raggedright}{}{0em}{}
\titleformat{\subsubsection}{\normalsize\bfseries\color{AtlasNavy}\raggedright}{}{0em}{}
\titlespacing*{\section}{0pt}{14pt}{6pt}\titlespacing*{\subsection}{0pt}{10pt}{5pt}
\pagestyle{fancy}\fancyhf{}\fancyhead[L]{\small\sffamily\color{AtlasGray}COMPLEXITY ATLAS}
\fancyhead[R]{\small\sffamily\color{AtlasGray}ENGLISH EDITION}\fancyfoot[C]{\small\thepage}\renewcommand{\headrulewidth}{.3pt}
\newcommand{\AtlasMath}[1]{\par\begingroup\centering\setbox0=\hbox{$\displaystyle #1$}\ifdim\wd0>1.4\linewidth\typeout{ATLAS WIDE FORMULA: \the\wd0}\fi\ifdim\wd0>\linewidth\resizebox{\linewidth}{!}{\box0}\else\box0\fi\par\endgroup}
\newcommand{\AtlasInlineMath}[1]{\begingroup\setbox0=\hbox{$#1$}\ifdim\wd0>.4\linewidth\endgroup\AtlasMath{#1}\else\endgroup$#1$\fi}
\pdfstringdefDisableCommands{\def\AtlasInlineMath#1{#1}}
\DeclareMathOperator{\polylog}{polylog}\DeclareMathOperator{\dist}{dist}\DeclareMathOperator{\diam}{diam}
\DeclareMathOperator{\rank}{rank}\DeclareMathOperator{\tr}{tr}\DeclareMathOperator{\diag}{diag}
\DeclareMathOperator{\prox}{prox}\DeclareMathOperator{\KL}{KL}\DeclareMathOperator{\Var}{Var}
\providecommand{\eps}{\varepsilon}\providecommand{\R}{\mathbb R}\providecommand{\E}{\mathbb E}
\providecommand{\mathbbm}[1]{\mathbf{#1}}\providecommand{\mathds}[1]{\mathbf{#1}}
\providecommand{\llbracket}{[\![}\providecommand{\rrbracket}{]\!]}
\begin{document}
\raggedright
'''
def mathclean(x):
    x=unicodedata.normalize('NFC',str(x or '').strip().strip('$'))
    greek={'α':'alpha','β':'beta','γ':'gamma','δ':'delta','ε':'varepsilon','ϵ':'varepsilon','ζ':'zeta','η':'eta','θ':'theta','κ':'kappa','λ':'lambda','μ':'mu','ν':'nu','ξ':'xi','π':'pi','ρ':'rho','σ':'sigma','τ':'tau','φ':'varphi','χ':'chi','ψ':'psi','ω':'omega','Γ':'Gamma','Δ':'Delta','Θ':'Theta','Λ':'Lambda','Π':'Pi','Σ':'Sigma','Φ':'Phi','Ω':'Omega'}
    for a,b in greek.items():x=x.replace(a,'\\'+b+' ')
    for a,b in {'∞':r'\infty ','≤':r'\le ','≥':r'\ge ','∈':r'\in ','∉':r'\notin ','×':r'\times ','→':r'\to ','↦':r'\mapsto ','∇':r'\nabla ','∂':r'\partial ','∑':r'\sum ','√':r'\sqrt ','≈':r'\approx ','≍':r'\asymp ','≲':r'\lesssim ','≳':r'\gtrsim ','≫':r'\gg ','≪':r'\ll ','≻':r'\succ ','⪰':r'\succeq ','⊂':r'\subset ','⊆':r'\subseteq ','ℓ':r'\ell ','−':'-','–':'-','—':'-','²':'^2','³':'^3','⁴':'^4','⁵':'^5','⁶':'^6','⁷':'^7','⁸':'^8','⁹':'^9','⁻':'^-','Õ':r'\widetilde O','Õ':r'\widetilde O','𝒳':r'\mathcal X','𝒰':r'\mathcal U','ᵀ':r'^{\mathsf T}','ᵈ':'^{d}','∘':r'\circ ','₀':'_0','₁':'_1','₂':'_2','₃':'_3','₄':'_4','₅':'_5','₆':'_6','₇':'_7','₈':'_8','₉':'_9'}.items():x=x.replace(a,b)
    x=re.sub(r'\^\s*-\s*(\d+)',r'^{-\1}',x)
    x=re.sub(r'\^\(([^()]*)\)',r'^{\1}',x)
    x=re.sub(r'(?<![A-Za-z\\])sqrt\(([^()]*)\)',r'\\sqrt{\1}',x)
    x=re.sub(r'(?<![A-Za-z\\])(log|exp|sin|cos|min|max|inf|sup)\b(?=\s*[({\[])',r'\\\1',x)
    x=x.replace('||',r'\|').replace('\x00','')
    if x.strip()==r'\sqrt':x=r'\sqrt{\vphantom{x}}'
    x=re.sub(r'\\begin\{(?:equation\*?|displaymath)\}|\\end\{(?:equation\*?|displaymath)\}','',x)
    return x.strip()

def display_math(x):
    x=mathclean(x)
    # Wrap long prose qualifications inside formulas without shrinking them to illegibility.
    def wrap_texts(src):
        out=[];pos=0
        while True:
            m=re.search(r'\\text\{',src[pos:])
            if not m:out.append(src[pos:]);break
            start=pos+m.start();j=pos+m.end();depth=1;k=j
            while k<len(src) and depth:
                if src[k]=='{' and (k==0 or src[k-1]!='\\'):depth+=1
                elif src[k]=='}' and (k==0 or src[k-1]!='\\'):depth-=1
                k+=1
            if depth:out.append(src[pos:]);break
            body=src[j:k-1];flat=re.sub(r'\\text\{([^{}]*)\}',r'\1',body)
            flat=flat.replace(r'\quad',' ').replace(r'\,',' ')
            out.append(src[pos:start])
            if len(flat)>60 and not re.search(r'\\[A-Za-z]|[{}]',flat):
                lines=textwrap.wrap(flat,width=56,break_long_words=False)
                out.append(r'\substack{'+r'\\'.join(r'\text{'+line+'}' for line in lines)+'}')
            else:out.append(src[start:k])
            pos=k
        return ''.join(out)
    x=wrap_texts(x)
    if r'\begin{' in x or r'\\' in x and r'\substack' not in x:return x
    # Top-level spacing marks in parameter domains provide safe line-break points.
    cuts=[];depth=0;left_depth=0;i=0;last=0
    while i<len(x):
        if x.startswith(r'\left',i):left_depth+=1
        elif x.startswith(r'\right',i):left_depth=max(0,left_depth-1)
        if x[i]=='{' and (i==0 or x[i-1]!='\\'):depth+=1
        elif x[i]=='}' and (i==0 or x[i-1]!='\\'):depth=max(0,depth-1)
        if x.startswith(r'\quad',i) and depth==0 and left_depth==0:
            cuts.append(x[last:i].strip());i+=len(r'\quad');last=i;continue
        i+=1
    cuts.append(x[last:].strip())
    def width(s):
        s=re.sub(r'\\(?:frac|dfrac|tfrac|left|right|bigl|bigr|Bigl|Bigr|mathrm|mathbb|mathcal|text|substack)','',s)
        s=re.sub(r'\\[A-Za-z]+','x',s)
        return len(re.sub(r'[{}\\]','',s))
    if len(cuts)>1 and sum(width(y) for y in cuts)>90:
        lines=[];line=[];w=0
        for part in cuts:
            pw=width(part)
            if line and w+pw>80:lines.append(r'\quad '.join(line));line=[];w=0
            line.append(part);w+=pw+3
        if line:lines.append(r'\quad '.join(line))
        return r'\begin{gathered}'+r'\\[3pt]'.join(lines)+r'\end{gathered}'
    return x

def is_formula(x):
    if not isinstance(x,str) or '$' in x or '://' in x or '`' in x:return False
    if not re.search(r'[\\_^=<>≤≥∈∞∇√α-ωΑ-Ω²³⁴⁵⁶⁷⁸⁹]',x):return False
    t=re.sub(r'\\(?:text|mathrm|operatorname|mathsf|mathcal|mathbb)\{[^}]*\}', '', x)
    t=re.sub(r'\\[A-Za-z]+', '',t)
    t=re.sub(r'\b(?:log|exp|sqrt|polylog|max|min|sup|inf|rank|det|tr|diag|ln)\b','',t)
    return not re.search(r'[A-Za-z]{4,}',t)

def escape(x):
    x=html.unescape(str(x)).replace('–','-').replace('—','-').replace('‑','-').replace('−','-')
    for a,b in {'，':', ','；':'; ','。':'.','：':': ','（':' (','）':') ','、':', ','【':'[','】':']','／':'/'}.items():x=x.replace(a,b)
    table={'\\':r'\textbackslash{}','&':r'\&','%':r'\%','$':r'\$','#':r'\#','_':r'\_','{':r'\{','}':r'\}','~':r'\textasciitilde{}','^':r'\textasciicircum{}'}
    out=[]
    for c in x:
        if c in 'αβγδεϵζηθκλμνξπρστφχψωΓΔΘΛΠΣΦΩ∞≤≥∈∉×→↦∇∂∑√≈≍≲≳≫≪≻⪰⊂⊆ℓ𝒳𝒰':out.append(r'\ensuremath{'+mathclean(c)+'}')
        elif c in '₀₁₂₃₄₅₆₇₈₉':out.append(r'\textsubscript{'+str('₀₁₂₃₄₅₆₇₈₉'.index(c))+'}')
        elif c=='ᵀ':out.append(r'\textsuperscript{T}')
        elif c in '²³⁴⁵⁶⁷⁸⁹':out.append(r'\textsuperscript{'+str('²³⁴⁵⁶⁷⁸⁹'.index(c)+2)+'}')
        else:out.append(table.get(c,c))
    return ''.join(out)
def prose_escape_math(x):
    symbols='αβγδεϵζηθκλμνξπρστφχψωΓΔΘΛΠΣΦΩ∞≤≥∈∉×→↦∇∂∑√≈≍≲≳≫≪≻⪰⊂⊆ℓ𝒳𝒰ᵀᵈ∘₀₁₂₃₄₅₆₇₈₉²³⁴⁵⁶⁷⁸⁹'
    chars=r'A-Za-z0-9_{}()\[\].,+*/^=<>:|!\-'
    pattern='['+chars+re.escape(symbols)+']*['+re.escape(symbols)+']['+chars+re.escape(symbols)+']*'
    out=[];last=0
    for m in re.finditer(pattern,x):
        out.append(escape(x[last:m.start()]));token=m.group()
        trailing=''
        while token.endswith(('.',',')):
            trailing=token[-1]+trailing;token=token[:-1]
        out.append('$'+mathclean(token)+'$'+escape(trailing));last=m.end()
    out.append(escape(x[last:]));return ''.join(out)

def prose_tex(x):
    x=str(x or '').replace(r'\[','$$').replace(r'\]','$$').replace(r'\(','$').replace(r'\)','$')
    # Parse emphasis before its embedded math, so bold labels containing notation
    # remain one well-formed unit rather than exposing literal Markdown markers.
    chunks=re.split(r'(\[\d+\]\(https?://[^\s)]+\)|https?://[^\s<>]+|\*\*[\s\S]*?\*\*|`[^`]+`|\$\$[\s\S]*?\$\$|\$[^$]*?\$)',x)
    out=[]
    for c in chunks:
        if not c:continue
        citation=re.fullmatch(r'\[(\d+)\]\((https?://[^\s)]+)\)',c)
        if citation:out.append(r'\href{'+citation.group(2).replace('%',r'\%')+'}{['+citation.group(1)+']}')
        elif c.startswith(('https://','http://')):out.append(r'\url{'+c.replace('%',r'\%')+'}')
        elif c.startswith('**') and c.endswith('**'):out.append(r'\textbf{'+prose_tex(c[2:-2])+'}')
        elif c.startswith('`') and c.endswith('`'):out.append(r'\texttt{'+escape(c[1:-1]).replace(r'\_',r'\_\allowbreak{}')+'}')
        elif c.startswith('$$') and c.endswith('$$'):out.append('\n\\AtlasMath{'+display_math(c[2:-2])+'}\n')
        elif c.startswith('$') and c.endswith('$'):
            formula=mathclean(c[1:-1])
            visible=re.sub(r'\\[A-Za-z]+','x',formula)
            visible=re.sub(r'[{}\\]','',visible)
            if len(visible)>58:out.append('\n\\AtlasMath{'+display_math(formula)+'}\n')
            else:out.append(r'\AtlasInlineMath{'+formula+'}')
        else:out.append(prose_escape_math(c))
    return ''.join(out)

def paragraphs(x):
    if x is None:return []
    if isinstance(x,str):return [x] if x.strip() else []
    if isinstance(x,list):return [str(v) for v in x if isinstance(v,(str,int,float)) and str(v).strip()]
    return []
def flatten_text(x):
    if isinstance(x,str):return x
    if isinstance(x,(int,float,bool)):return str(x)
    if isinstance(x,list):return '; '.join(flatten_text(v) for v in x if v is not None)
    if isinstance(x,dict):return '; '.join(k.replace('_',' ')+': '+flatten_text(v) for k,v in x.items() if v is not None and v!='' and v!=[] and v!={} and k not in ['id','code'])
    return ''
def merge(a,b):
    out=copy.deepcopy(a)
    for k,v in b.items():out[k]=merge(out[k],v) if isinstance(v,dict) and isinstance(out.get(k),dict) else copy.deepcopy(v)
    return out
def unique(seq):
    seen=set();out=[]
    for x in seq:
        key=json.dumps(x,sort_keys=True,ensure_ascii=False)
        if key not in seen:seen.add(key);out.append(x)
    return out
def scope_label(b):
    role=b.get('evidence_role','')
    labels={'deterministic':'Deterministic witness','randomized':'Randomized witness','unrestricted_randomized':'All randomized adaptive algorithms','unrestricted_deterministic':'All deterministic adaptive algorithms','restricted_randomized':'The stated restricted randomized class','restricted_deterministic':'The stated restricted deterministic class','not_certified':'Witness type not certified'}
    x=b.get('witness_type') or b.get('lower_scope_type')
    text=labels.get(x,x or '')
    if role:text=(role.replace('_',' ').capitalize()+': '+text).strip(': ')
    return text or flatten_text(b.get('algorithm_class_scope')) or 'Algorithm scope stated in the evidence below'
def document_nodes(p):
    n=[]
    def h(level,s):n.append(('h'+str(level),s))
    def para(s):
        if s:n.append(('math' if is_formula(str(s)) else 'p',str(s)))
    def math(s):
        if s:
            st=str(s)
            if '$' in st or re.search(r'(?<!\\)\b[A-Za-z]{4,}\s+[A-Za-z]{3,}\b',re.sub(r'\\text\{[^}]*\}','',st)):para(st)
            else:n.append(('math',st))
    def field(k,v):
        if v:
            if is_formula(v):para('**'+k+'.**');math(v)
            else:para('**'+k+'.** '+str(v))
    def ps(xs):
        for x in paragraphs(xs):para(x)
    views={v['view_id']:v for v in p['views']}
    blabel={b['id']:'B'+str(i+1) for i,b in enumerate(p['bounds'])}
    rlabel={r['id']:str(i+1) for i,r in enumerate(p['references'])}
    qlabel={q['id']:'Q'+str(i+1) for i,q in enumerate(p['quantities'])}
    plabel={r['resource_projection_id']:r for r in p['resource_projections']}
    evidence={e['id']:e for e in p['evidence']}
    proofs={d['proof_id']:d for d in p.get('proofs',[])}
    proof_labels={pid:'A'+str(i+1) for i,pid in enumerate(proofs)}
    sources={r['id']:r for r in p['references']}
    def cites(refs):return ' '.join('['+rlabel[x]+']('+sources[x]['url']+')' for x in refs if x in rlabel)
    h(1,p['title']);field('Setting ID','`'+p['setting_id']+'`')
    para(TOPICS.get(p['primary_domain'],p['primary_domain'].replace('_',' ').title()))
    para(p.get('summary'))
    ss=p['summary_status'];field('Status','; '.join(x['label'] for x in ss['badges']+ss['special_statuses']))
    if len(ss['gap_classes'])>1:field('Gap classes present','; '.join(STATUS[g] for g in ss['gap_classes']))
    para(ss.get('headline_note'))
    if ss.get('headline_note'):
        for detail in ss.get('gap_details',[]):field('Additional gap: '+views[detail['view_id']]['label']+' / '+detail['region'],detail.get('expression'))
    elif ss.get('gap_details'):
        para('The regional bracket below specifies the quantified gaps and their parameter dependence.')
    classification=p.get('_classification',{})
    for axis in ['TASK','MODEL','ORACLE','ALGORITHMS','OUTPUT','METRIC','GUARANTEE','RESOURCE']:
        tags=[t for t in classification.get('tags',[]) if t['axis']==axis]
        if tags:
            field(axis+' tags','; '.join(dict.fromkeys(t['group'].replace('_',' ') + ': ' + t['label'] for t in tags)))
    h(2,'1. Setting specification')
    display=p.get('display_specification') or p['common_specification']
    for axis,label in AXES.items():
        h(3,label);section=display.get(axis,{})
        lines=section.get('description_paragraphs',[])
        if lines:ps(lines)
        elif axis in ['task','metric']:
            math(section.get('formulation') or section.get('base_expression') or section.get('formula_latex'))
        else:
            for k,v in section.items():
                if isinstance(v,str) and not k.endswith(('_ref','_id')) and k not in ['id','code']:field(k.replace('_',' ').capitalize(),v)
    h(3,'Algorithm views and success guarantees')
    for v in p['views']:
        if len(p['views'])>1:h(4,v['label'])
        a=v['algorithms'];ps(a.get('description_paragraphs'))
        if not a.get('description_paragraphs'):
            for k in ['randomization','adaptivity','restrictions','internal_computation']:field(k.replace('_',' ').capitalize(),flatten_text(a.get(k)))
        for g in v['guarantees']:
            ps(g.get('description_paragraphs'))
            if not g.get('description_paragraphs'):math(g.get('complete_expression') or g.get('formula_latex'));field('Guarantee',flatten_text(g.get('aggregation_order')))
        for text in v.get('display_qualifications',[]):para(text)
        field('Budget convention',flatten_text(v.get('budget',{}).get('budget_semantics')))
    h(2,'2. Notation and parameters')
    seen=set()
    for s in p.get('symbols',[]):
        sig=(s.get('symbol_latex'),s.get('meaning'),s.get('domain'),s.get('definition'))
        if sig in seen:continue
        seen.add(sig)
        text='$'+mathclean(s.get('symbol_latex'))+'$: '+str(s.get('meaning',''))
        if s.get('domain'):text+=' **Domain:** '+str(s['domain']).rstrip('.')+'.'
        para(text)
        d=s.get('definition')
        if d and str(d) not in str(s.get('meaning','')):para(d)
    h(2,'3. Complexity bracket')
    h(3,'Compared quantities')
    for q in p['quantities']:
        h(4,qlabel[q['id']]+' - '+q.get('kind','quantity').replace('_',' '))
        if len(views)>1:field('View',views[q['view_id']]['label'])
        math(q.get('expression_latex') or q.get('expression'))
        field('Definition',q.get('label'));field('Scope',q.get('analysis_scope'))
        field('Optimization direction',q.get('optimization_direction'))
        ps(q.get('display_notation_note'));ps(q.get('definition_note'))
        if q.get('metric_contract'):field('Metric contract',flatten_text(q['metric_contract']))
        if q.get('resource_contract'):field('Resource contract',flatten_text(q['resource_contract']))
        if q.get('interpretation'):para(q['interpretation'])
    comps={c['comparison_id']:c for c in p['comparisons']}
    for i,row in enumerate(p['bracket_rows'],1):
        cs=[comps[x] for x in row['comparison_ids']];c=cs[0];br=c['bracket']
        h(3,'R'+str(i)+' - '+c.get('label','Parameter regime'))
        field('Region',c.get('predicate_text'))
        if len(views)>1:field('Views','; '.join(views[v]['label'] for v in dict.fromkeys(row['view_ids'])))
        field('Quantity','; '.join(dict.fromkeys(qlabel.get(x['quantity_id'],x['quantity_id'] or 'Not specified') for x in cs)))
        rp=plabel[c['resource_projection_id']];field('Resource',rp.get('description') or rp.get('expression') or 'Joint resource budget')
        field('Status',STATUS.get(c['status']['code'],c['status']['code']))
        joint=bool(br.get('achievable_refs') or br.get('necessary_refs') or c['status']['code']=='joint_budget_unclosed')
        if joint:
            for key,title in [('achievable_refs','Achievable budgets'),('necessary_refs','Necessary constraints')]:field(title,', '.join(blabel.get(x,x) for x in br.get(key,[])) or 'No admitted claim in this comparison')
        else:
            for side,title in [('lower','Lower bound'),('upper','Upper bound')]:
                env=br.get('envelopes',{}).get(side)
                refs=unique(x for cc in cs for x in cc['bracket'].get(side+'_refs',[]))
                if env:field(title,', '.join(blabel.get(x,x) for x in refs) or ('Nonnegativity of the compared quantity' if env.get('basis')=='nonnegativity' else 'Admitted envelope'));math(env.get('expression_latex') or env.get('expression'))
                elif refs:field(title,', '.join(blabel.get(x,x) for x in refs))
                elif c['status']['code'] not in ['infinite_complexity','infeasible_task']:field(title,'No admitted bound for this comparison')
        field('Gap or comparison',br.get('ratio_or_gap'))
        field('Comparison argument',br.get('envelope_certificate'))
    h(2,'4. Bounds and supporting evidence')
    shared={}
    shared_keys=['conditions','dimension_conditions','oracle_mapping','guarantee_mapping','output_mapping','resource_mapping']
    for key in shared_keys:
        vals=[b.get('applicability',{}).get(key) if isinstance(b.get('applicability'),dict) else None for b in p['bounds']]
        if vals and vals[0] and all(v==vals[0] for v in vals):shared[key]=vals[0]
    if shared:
        para("The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.")
        for key,value in shared.items():field(key.replace('_',' ').capitalize(),flatten_text(value))
    for b in p['bounds']:
        h(3,blabel[b['id']]+' - '+str(b.get('method') or b.get('algorithm_or_hard_family') or b.get('direction','Claim')).strip())
        field('Admission','Included in the bracket' if b.get('included_in_bracket') else ('Eligible evidence; not selected in the displayed bracket' if b.get('eligible_for_bracket') else 'Not admitted to the bracket; retained for traceability'))
        field('Direction',b.get('direction'))
        if len(views)>1:field('View',views[b['view_id']]['label'])
        field('Witness or lower-bound scope',scope_label(b))
        field('Algorithm-scope qualification',b.get('witness_type_note') or b.get('lower_scope_type_note'))
        math(b.get('formula_latex'));field('Meaning of the inequality',b.get('direction_explanation'))
        for qkey,formula in b.get('formula_by_quantity',{}).items():field(qkey.replace('_',' ').capitalize(),formula)
        field('Sources',cites(b.get('source_refs',[])))
        ap=b.get('applicability',{})
        if not isinstance(ap,dict):
            field('Applicability',flatten_text(ap));ap={}
        for k,title in [('conditions','Conditions'),('dimension_conditions','Dimension conditions'),('oracle_mapping','Oracle correspondence'),('guarantee_mapping','Guarantee conversion'),('output_mapping','Output rule'),('resource_mapping','Resource conversion')]:
            val=ap.get(k)
            if val and k not in shared:field(title,flatten_text(val))
        if b.get('resource_costs'):
            para('**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.')
            for resource,value in b['resource_costs'].items():field(resource.replace('_',' '),value)
        field('Constants',b.get('hidden_constants'));field('Logarithmic factors',flatten_text(b.get('hidden_logs')))
        if b.get('derivation'):field('Derivation',b['derivation'])
        if b.get('proof_refs'):field('Local argument',', '.join(proof_labels.get(x,x) for x in b['proof_refs']))
        for eid in b.get('evidence_refs',[]):
            e=evidence.get(eid,{})
            if e.get('kind')=='local_argument':continue
            sr=e.get('source_refs') or [e.get('source_ref')]
            loc=e.get('location') or flatten_text(e.get('locator'))
            if loc:field('Source location',cites(sr)+' '+loc)
            ps(e.get('statement_summary'));ps(e.get('applicability_review'));ps(e.get('notes'))
    if proofs:
        h(2,'5. Local arguments')
        for d in proofs.values():
            h(3,proof_labels[d['proof_id']]+' - '+d.get('title','Derivation'))
            field('Scope',flatten_text(d.get('scope')));field('Algorithm scope',flatten_text(d.get('algorithm_scope')))
            ps(d.get('statement'));ps(d.get('body') or d.get('proof'));field('Limits of the argument',flatten_text(d.get('limitations')))
            field('Sources',cites(d.get('source_refs',[])))
    if p['references']:h(2,'References')
    for r in p['references']:
        author=flatten_text(r.get('authors'));title=r.get('title','');year=str(r.get('year') or '')
        para('['+rlabel[r['id']]+'] '+'. '.join(x for x in [author,title,year,r.get('version','')] if x)+'.')
        if r.get('url'):para(r['url'])
    return n
def to_md(nodes):
    out=[]
    for kind,x in nodes:
        if kind.startswith('h'):out.append('#'*int(kind[1:])+' '+x)
        elif kind=='math':out.append('$$\n'+display_math(x)+'\n$$')
        else:out.append(x)
    return '\n\n'.join(out)+'\n'
def to_tex(nodes):
    out=[PREAMBLE]
    for kind,x in nodes:
        if kind=='h1':out.append(r'{\LARGE\bfseries\sffamily\color{AtlasNavy} '+prose_tex(x)+r'\par}\vspace{5pt}')
        elif kind=='h2':
            # Complexity starts with two nested headings; keep all three together.
            reserve=12 if x.endswith('Complexity bracket') else 7
            out.append(r'\needspace{'+str(reserve)+r'\baselineskip}\section{'+prose_tex(x)+'}')
        elif kind=='h3':out.append(r'\needspace{4\baselineskip}\subsection{'+prose_tex(x)+'}')
        elif kind=='h4':out.append(r'\needspace{4\baselineskip}\subsubsection{'+prose_tex(x)+'}')
        elif kind=='math':out.append(r'\AtlasMath{'+display_math(x)+'}')
        else:out.append(prose_tex(x)+'\n')
    return '\n'.join(out)+'\n\\end{document}\n'
def compile_pdf(tex):
    tex=pathlib.Path(tex);logs=[]
    digest=hashlib.sha256(tex.read_bytes()).hexdigest()
    cache=tex.with_suffix('.compile.json')
    pdf=tex.with_suffix('.pdf')
    def complete_pdf():
        if not pdf.exists():return False
        data=pdf.read_bytes()
        return data.startswith(b'%PDF-') and data.rstrip().endswith(b'%%EOF') and b'startxref' in data[-150:]
    if cache.exists() and complete_pdf():
        previous=json.loads(cache.read_text())
        if previous.get('tex_sha256')==digest and previous.get('returncode')==0:
            if not previous.get('pdf_sha256') or previous['pdf_sha256']==hashlib.sha256(pdf.read_bytes()).hexdigest():return previous
    for extension in ['.aux','.out','.toc']:
        tex.with_suffix(extension).unlink(missing_ok=True)
    for i in range(2):
        r=subprocess.run(['xelatex','-interaction=nonstopmode','-halt-on-error','-file-line-error',tex.name],cwd=tex.parent,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
        logs.append(r.stdout)
        if r.returncode:break
    text='\n'.join(logs);bad=[line for line in text.splitlines() if any(x in line for x in ['Overfull \\hbox','Overfull \\vbox','Missing character','Undefined control sequence','LaTeX Error','ATLAS WIDE FORMULA'])]
    code=r.returncode
    if code==0 and not complete_pdf():
        code=1;text+='\nThe generated PDF is incomplete; compilation has not produced a valid final trailer.'
    result={'file':str(tex),'returncode':code,'warnings':bad,'error_tail':text[-5000:] if code else '', 'tex_sha256':digest}
    if code==0:result['pdf_sha256']=hashlib.sha256(pdf.read_bytes()).hexdigest()
    if code==0:cache.write_text(json.dumps(result,indent=2))
    return result
def main():
    ap=argparse.ArgumentParser();ap.add_argument('input');ap.add_argument('--output',default='.');ap.add_argument('--pdf',action='store_true');ap.add_argument('--workers',type=int,default=4);ap.add_argument('--setting');a=ap.parse_args()
    raw=json.loads(pathlib.Path(a.input).read_text());settings=raw.get('settings',[raw]);root=pathlib.Path(a.output);root.mkdir(parents=True,exist_ok=True);texfiles=[]
    for p in settings:
        if a.setting and p['setting_id']!=a.setting:continue
        folder=root/'settings'/p['setting_id'];folder.mkdir(parents=True,exist_ok=True);stem=folder/p['setting_id'];nodes=document_nodes(p)
        stem.with_suffix('.json').write_text(json.dumps(p,ensure_ascii=False,indent=2));stem.with_suffix('.md').write_text(to_md(nodes));stem.with_suffix('.tex').write_text(to_tex(nodes));texfiles.append(stem.with_suffix('.tex'))
    if a.pdf:
        with concurrent.futures.ThreadPoolExecutor(max_workers=a.workers) as pool:
            results=list(pool.map(compile_pdf,texfiles))
        (root/'compilation_report.json').write_text(json.dumps(results,indent=2))
        print(json.dumps({'compiled':len(results),'failed':sum(x['returncode']!=0 for x in results),'with_warnings':sum(bool(x['warnings']) for x in results)}))
    else:print(json.dumps({'rendered':len(texfiles)}))
if __name__=='__main__':main()
