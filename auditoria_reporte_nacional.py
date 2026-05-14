import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import pandas as pd
import re
import unicodedata

APP_TITLE = "Auditoría de Reporte Nacional — MSE&V"

# -----------------------------
# Catálogos base ampliados
# -----------------------------
PROGRAMAS_NACIONALES = [
    "ANTIOQUIA / CHOCÓ",
    "BOGOTÁ / CUNDINAMARCA",
    "CARIBE",
    "NARIÑO",
    "SANTANDER",
    "VALLE",
]

PROYECTOS_NACIONALES = [
    "UNICEF JÓVENES 2024",
    "SOS VENEZUELA_REUNIFICACIÓN",
    "SEMILLAS DE CUIDADO - PSA ALEMANIA",
    "ECHO - A TU LADO 2025",
    "CHILHOOD MATTERS",
    "CHILDHOOD MATTERS",
    "VAMOS A JUGAR LIMPIO Y EN PAZ - FIFA 2025",
    "AKELIUS",
    "SDIS",
    "CAMINOS DE CUIDADO: HACIA UNA MIGRACIÓN SEGURA, DIGNA E INCLUSIVA",
    "CAMINOS DE CUIDADO:  HACIA UNA MIGRACIÓN SEGURA, DIGNA E INCLUSIVA",
    "UNIDOS POR LA PROTECCIÓN INFANTIL- MULTIPAÍS 1",
]

SERVICIOS = [
    "EDUCACIÓN PRIMARIA Y SECUNDARIA (EDU)",
    "EMPODERAMIENTO FAMILIAR DIRECTO (DFE)",
    "EMPODERAMIENTO COMUNITARIO PARA EL EMPODERAMIENTO FAMILIAR (CFE)",
    "ABOGACÍA (ADV)",
    "ACCIÓN HUMANITARIA (HA)",
    "OTRA MODALIDAD DE CUIDADO ALTERNATIVO (OAC)",
    "CUIDADO ALTERNATIVO TEMPORAL (CAT)",
    "GESTIÓN DE CASOS (GC)",
    "ALBERGUE",
    "ESPACIOS INTEGRALES",
    "SIN INFORMACIÓN",
    "SIN_INFORMACIÓN",
    "NINGUNO",
]

TIPOS_PARTICIPANTE = [
    "NIÑO, NIÑA, ADOLESCENTE, JOVEN",
    "NIÑO, NIÑA, ADOLESCENTE",
    "CUIDADOR/A PRINCIPAL",
    "CUIDADOR/A SECUNDARIO",
    "LÍDER/LIDERESA COMUNITARIA",
    "AGENTE COMUNITARIO",
    "EQUIPO COMUNITARIO DE PROTECCIÓN INFANTIL",
    "FUNCIONARIO PÚBLICO",
    "ADULTO/CUIDADOR"
]

SEXO = ["MUJER", "HOMBRE", "INTERSEXUAL"]
GENERO = ["FEMENINO", "MASCULINO", "LGTBIQ+", "OTRO"]
GRUPO_ETNICO = [
    "AFROCOLOMBIANO",
    "MESTIZO",
    "INDÍGENA",
    "COMUNIDAD NEGRA",
    "ROMM/GITANO",
    "PALENQUERO",
    "NO SE RECONOCE EN NINGUNA DE LAS ANTERIORES",
    "OTRO",
    "AFROCOLOMBIANO"
]
NACIONALIDAD = [
    "VENEZOLANO/A",
    "COLOMBIANO/A",
    "COLOMBO VENEZOLANO/A",
    "ECUATORIANO/A",
    "RIESGO DE APATRIDIA",
    "OTRA",
]
PERFIL_PROTECCION = [
    "INTEGRANTE DE LA FAMILIA EN RIESGO",
    "NIÑO, NIÑA Y/O ADOLESCENTE NO ACOMPAÑADOS (MENORES DE 18 AÑOS)",
    "N/A",
    "NO APLICA",
    "SIN_INFORMACIÓN" ,
    "NIÑO, NIÑA Y/O ADOLESCENTE EN PARD EN MODALIDAD INSTITUCIONAL" ,
    "NIÑO, NIÑA Y/O ADOLESCENTE EN PARD EN MODALIDAD FAMILIAR"
]
ESTATUS_MIGRATORIO = ["REGULAR", "IRREGULAR", "NO APLICA", "NO_APLICA"]
TIPO_PROYECTO = ["PROYECTO HUMANITARIO", "PROYECTO DE DESARROLLO"]
ACCION_REALIZAR = [
    "ALBERGUE FAMILIAR",
    "ESPACIOS INTEGRALES",
    "CUIDADO ALTERNATIVO TEMPORAL/GESTIÓN DE CASOS",
    "CUIDADO ALTERNATIVO TEMPORAL",
    "GESTIÓN DE CASOS",
    "ORIENTACIÓN"
]

DOC_LONGITUDES = {
    "CÉDULA DE CIUDADANÍA": (6, 10),
    "TARJETA DE IDENTIDAD": (8, 11),
    "REGISTRO CIVIL": (5, 20),
    "CÉDULA DE EXTRANJERÍA": (6, 12),
    "PASAPORTE": (5, 17),
    "CÉDULA VENEZOLANA": (7, 9),
    "PERMISO ESPECIAL DE PERMANENCIA": (15, 16),
    "PERMISO DE PROTECCIÓN TEMPORAL": (7, 16),
    "REGISTRO ÚNICO DE MIGRANTES VENEZOLANOS": (7, 15),
    "ACTA DE NACIMIENTO": (1, 20),
    "CERTIFICADO NACIDO VIVO": (1, 20),
    "OTRO": (1, 30),
}
DOC_SIN_NUMERO = {"NO POSEE", "SIN DOCUMENTACIÓN POR PÉRDIDA"}

DEP_MUNI = {
    "ANTIOQUIA": {"NECOCLI", "NECOCLÍ"},
    "LA GUAJIRA": {"RIOHACHA", "MAICAO"},
    "NARIÑO": {"IPIALES"},
    "NORTE DE SANTANDER": {"CUCUTA", "CÚCUTA" , "TIBÚ" , "LA PLAYA" , "ÁBREGO" , "OCAÑA" },
    "SANTANDER": {"BUCARAMANGA", "PIEDECUESTA" , "FLORIDABLANCA" , "GIRÓN" },
    "CHOCO": {"QUIBDO", "QUIBDÓ"},
    "BOGOTA": {"BOGOTA", "BOGOTÁ"},
    "VALLE DEL CAUCA": {"CALI", "JAMUNDI", "JAMUNDÍ"},
}

SEVERITY_ORDER = {"CRÍTICO": 1, "ALTO": 2, "ADVERTENCIA": 3, "INFO": 4}
SEVERITY_COLORS = {
    "CRÍTICO": "#c0392b",
    "ALTO": "#e67e22",
    "ADVERTENCIA": "#b7950b",
    "INFO": "#2980b9",
}

SCHEMA = {
    "NÚMERO CONSECUTIVO DEL PARTICIPANTE": ["NÚMERO CONSECUTIVO DEL PARTICIPANTE"],
    "ID DEL PARTICIPANTE": ["ID DEL PARTICIPANTE (NO MODIFICAR)", "ID DEL PARTICIPANTE", "ID DEL PARTICIPANTE (FORMULADA)"],
    "PROGRAMA": ["PROGRAMA"],
    "PROYECTO": ["PROYECTO"],
    "SERVICIO PRINCIPAL": ["SERVICIO PRINCIPAL"],
    "SERVICIO SECUNDARIO": ["SERVICIO SECUNDARIO"],
    "SERVICIO TERCIARIO": ["SERVICIO TERCIARIO"],
    "TIPO DE PARTICIPANTE": ["TIPO DE PARTICIPANTE", "TIPO DE PARTICIPANTE (NO MODIFICAR)"],
    "FECHA DE INGRESO": ["FECHA DE INGRESO (DD/MM/AA)", "FECHA DE INGRESO"],
    "MES/AÑO DE INGRESO": ["MES/AÑO DE INGRESO"],
    "DEPARTAMENTO": ["DEPARTAMENTO"],
    "MUNICIPIO": ["MUNICIPIO"],
    "NOMBRE DEL PARTICIPANTE": ["NOMBRE DEL PARTICIPANTE", "NOMBRE DEL PARTICIPANTE (NO MODIFICAR)"],
    "APELLIDO DEL PARTICIPANTE": ["APELLIDO DEL PARTICIPANTE", "APELLIDO DEL PARTICIPANTE (NO MODIFICAR)"],
    "NOMBRE Y APELLIDO DEL PARTICIPANTE": [
        "NOMBRE Y APELLIDO DEL PARTICIPANTE (NO MODIFICAR)",
        "NOMBRE Y APELLIDO DEL PARTICIPANTE",
        "NOMBRE Y APELLIDO DEL PARTICIPANTE (FORMULADA)",
    ],
    "TIPO DE DOCUMENTO DEL PARTICIPANTE": ["TIPO DE DOCUMENTO DEL PARTICIPANTE", "TIPO DE DOCUMENTO DEL PARTICIPANTE (NO MODIFICAR)"],
    "NÚMERO DE DOCUMENTO DE IDENTIDAD DEL PARTICIPANTE": [
        "NÚMERO DE DOCUMENTO DE IDENTIDAD DEL PARTICIPANTE",
        "NÚMERO DE DOCUMENTO DE IDENTIDAD DEL PARTICIPANTE (NO MODIFICAR)",
    ],
    "EDAD DEL PARTICIPANTE": ["EDAD DEL PARTICIPANTE"],
    "GRUPO ETARIO INTERNO": ["GRUPO ETARIO INTERNO (NO MODIFICAR)", "GRUPO ETARIO INTERNO"],
    "SEXO DEL PARTICIPANTE": ["SEXO DEL PARTICIPANTE"],
    "GÉNERO DEL PARTICIPANTE": ["GÉNERO DEL PARTICIPANTE"],
    "GRUPO ÉTNICO DEL PARTICIPANTE": ["GRUPO ÉTNICO DEL PARTICIPANTE"],
    "NACIONALIDAD DEL PARTICIPANTE": ["NACIONALIDAD DEL PARTICIPANTE"],
    "PERFIL ESPECÍFICO DE PROTECCIÓN": ["PERFIL ESPECÍFICO DE PROTECCIÓN"],
    "ESTATUS MIGRATORIO DEL PARTICIPANTE": ["ESTATUS MIGRATORIO DEL PARTICIPANTE", "ESTATUS DE RESIDENCIA DEL PARTICIPANTE", "ESTATUS MIGRATORIO"],
    "TIPO DE PROYECTO": ["TIPO DE PROYECTO"],
    "ACCIÓN A REALIZAR": ["ACCIÓN A REALIZAR"],
}

REQUIRED = [
    "ID DEL PARTICIPANTE", "PROGRAMA", "PROYECTO", "SERVICIO PRINCIPAL",
    "TIPO DE PARTICIPANTE", "DEPARTAMENTO", "MUNICIPIO", "NOMBRE DEL PARTICIPANTE",
    "APELLIDO DEL PARTICIPANTE", "NOMBRE Y APELLIDO DEL PARTICIPANTE",
    "TIPO DE DOCUMENTO DEL PARTICIPANTE", "EDAD DEL PARTICIPANTE", "SEXO DEL PARTICIPANTE",
    "GÉNERO DEL PARTICIPANTE", "GRUPO ÉTNICO DEL PARTICIPANTE", "NACIONALIDAD DEL PARTICIPANTE",
]

# -----------------------------
# Utilidades
# -----------------------------
def normalize_spaces(text: str) -> str:
    return re.sub(r"\s+", " ", str(text).replace("\n", " ").replace("\r", " ")).strip()


def strip_accents(text: str) -> str:
    return "".join(ch for ch in unicodedata.normalize("NFKD", str(text)) if not unicodedata.combining(ch))


def canon(text) -> str:
    if text is None or (isinstance(text, float) and pd.isna(text)):
        return ""
    s = normalize_spaces(text).upper()
    s = strip_accents(s)
    s = s.replace("_", " ")
    s = re.sub(r"[^A-Z0-9\(\)\+\-\/ ]+", " ", s)
    return normalize_spaces(s)


def literal(text) -> str:
    if text is None or (isinstance(text, float) and pd.isna(text)):
        return ""
    s = normalize_spaces(text)
    if s.lower() in {"(en blanco)", "en blanco", "nan", "none", "null"}:
        return ""
    return s.upper()


def is_empty(val) -> bool:
    return literal(val) == ""


def parse_num(val):
    if is_empty(val):
        return None
    try:
        txt = str(val).strip().replace(".", "").replace(",", ".") if re.match(r"^\d{1,3}(\.\d{3})+,\d+$", str(val).strip()) else str(val).strip().replace(",", ".")
        return float(txt)
    except Exception:
        try:
            return float(pd.to_numeric(val))
        except Exception:
            return None


def limpio_doc(val) -> str:
    if is_empty(val):
        return ""
    s = str(val).strip()
    # conservar x10 scientific notation expanded if pandas left it that way as text
    if re.match(r"^[0-9]+([\.,][0-9]+)?E\+[0-9]+$", s.upper()):
        try:
            s = format(float(s), ".0f")
        except Exception:
            pass
    return re.sub(r"[^0-9A-Za-z]", "", s)


def parse_clipboard(text: str) -> pd.DataFrame:
    text = text.replace("\ufeff", "")
    lines = [ln for ln in text.splitlines() if normalize_spaces(ln)]
    lines = [ln for ln in lines if literal(ln) != "TOTAL GENERAL"]
    clean = "\n".join(lines)
    df = pd.read_csv(pd.io.common.StringIO(clean), sep="\t", dtype=str)
    df = df.fillna("")
    return df


def resolve_columns(df: pd.DataFrame):
    resolved = {}
    canon_cols = {col: canon(col) for col in df.columns}
    for target, aliases in SCHEMA.items():
        found = None
        for alias in aliases:
            key = canon(alias)
            for real, ckey in canon_cols.items():
                if ckey == key:
                    found = real
                    break
            if found:
                break
        resolved[target] = found
    return resolved


def validate_in_list(value, allowed):
    if is_empty(value):
        return True
    val = canon(value)
    allowed_can = {canon(x) for x in allowed}
    return val in allowed_can


def expected_group_from_age(age):
    if age is None:
        return None
    if age <= 5:
        return "0-5 AÑOS"
    if age <= 12:
        return "6-12 AÑOS"
    if age <= 17:
        return "13-17 AÑOS"
    if age <= 28:
        return "18-28 AÑOS"
    return "+28 AÑOS"


def add_error(rows, fila, pid, columna, tipo, severidad, categoria, detalle):
    rows.append({
        "Fila": fila,
        "ID del Participante": pid,
        "Columna": columna,
        "Tipo de error": tipo,
        "Severidad": severidad,
        "Categoría": categoria,
        "Detalle": detalle,
    })


def audit_df(df: pd.DataFrame):
    resolved = resolve_columns(df)
    errors = []

    # faltantes estructurales
    for req in REQUIRED:
        if not resolved.get(req):
            add_error(errors, "N/A", "", req, "Columna esperada no encontrada", "ALTO", "Estructura",
                      f'Falta la columna "{req}" en la tabla pegada.')

    # columnas inesperadas solo informativas si realmente no se homologaron
    all_aliases = {canon(a) for aliases in SCHEMA.values() for a in aliases}
    for col in df.columns:
        if canon(col) not in all_aliases:
            add_error(errors, "N/A", "", col, "Columna no esperada", "INFO", "Estructura",
                      f'La columna "{col}" no hace parte del esquema definido para esta auditoría.')

    id_col = resolved.get("ID DEL PARTICIPANTE")
    doc_type_col = resolved.get("TIPO DE DOCUMENTO DEL PARTICIPANTE")
    doc_num_col = resolved.get("NÚMERO DE DOCUMENTO DE IDENTIDAD DEL PARTICIPANTE")

    seen_ids = {}
    seen_docs = {}

    for idx, row in df.iterrows():
        fila = idx + 2
        pid = literal(row.get(id_col, "")) if id_col else ""
        if sum(0 if is_empty(v) else 1 for v in row.tolist()) < 3:
            continue

        # completud
        for req in REQUIRED:
            col = resolved.get(req)
            if col and is_empty(row.get(col, "")):
                add_error(errors, fila, pid, req, "Campo obligatorio vacío", "CRÍTICO", "Completud",
                          f'El campo "{req}" está vacío.')

        # catálogos comunes
        cat_checks = [
            ("PROGRAMA", PROGRAMAS_NACIONALES),
            ("PROYECTO", PROYECTOS_NACIONALES),
            ("SERVICIO PRINCIPAL", SERVICIOS),
            ("SERVICIO SECUNDARIO", SERVICIOS),
            ("SERVICIO TERCIARIO", SERVICIOS),
            ("TIPO DE PARTICIPANTE", TIPOS_PARTICIPANTE),
            ("SEXO DEL PARTICIPANTE", SEXO),
            ("GÉNERO DEL PARTICIPANTE", GENERO),
            ("GRUPO ÉTNICO DEL PARTICIPANTE", GRUPO_ETNICO),
            ("NACIONALIDAD DEL PARTICIPANTE", NACIONALIDAD),
            ("PERFIL ESPECÍFICO DE PROTECCIÓN", PERFIL_PROTECCION),
            ("ESTATUS MIGRATORIO DEL PARTICIPANTE", ESTATUS_MIGRATORIO),
            ("TIPO DE PROYECTO", TIPO_PROYECTO),
            ("ACCIÓN A REALIZAR", ACCION_REALIZAR),
        ]
        for field, allowed in cat_checks:
            col = resolved.get(field)
            if col and not validate_in_list(row.get(col, ""), allowed):
                add_error(errors, fila, pid, field, "Valor fuera de lista", "ALTO", "Catálogo",
                          f'"{literal(row.get(col, ""))}" no pertenece al catálogo esperado.')

        # coherencia sexo/género
        sexo = canon(row.get(resolved.get("SEXO DEL PARTICIPANTE"), ""))
        genero = canon(row.get(resolved.get("GÉNERO DEL PARTICIPANTE"), ""))
        if sexo == "MUJER" and genero == "MASCULINO":
            add_error(errors, fila, pid, "SEXO/GÉNERO", "Incoherencia sexo-género", "ALTO", "Coherencia", "MUJER con género MASCULINO.")
        if sexo == "HOMBRE" and genero == "FEMENINO":
            add_error(errors, fila, pid, "SEXO/GÉNERO", "Incoherencia sexo-género", "ALTO", "Coherencia", "HOMBRE con género FEMENINO.")

        # nombre completo
        nom = row.get(resolved.get("NOMBRE DEL PARTICIPANTE"), "") if resolved.get("NOMBRE DEL PARTICIPANTE") else ""
        ape = row.get(resolved.get("APELLIDO DEL PARTICIPANTE"), "") if resolved.get("APELLIDO DEL PARTICIPANTE") else ""
        full = row.get(resolved.get("NOMBRE Y APELLIDO DEL PARTICIPANTE"), "") if resolved.get("NOMBRE Y APELLIDO DEL PARTICIPANTE") else ""
        if not is_empty(nom) and not is_empty(ape) and not is_empty(full):
            expected = canon(f"{nom} {ape}")
            if canon(full) != expected:
                add_error(errors, fila, pid, "NOMBRE Y APELLIDO DEL PARTICIPANTE", "Nombre completo inconsistente", "ADVERTENCIA", "Coherencia",
                          f'Se esperaba "{normalize_spaces(str(nom) + " " + str(ape))}" pero figura "{normalize_spaces(full)}".')

        # edad/tipo/grupo
        edad = parse_num(row.get(resolved.get("EDAD DEL PARTICIPANTE"), "")) if resolved.get("EDAD DEL PARTICIPANTE") else None
        tipo = canon(row.get(resolved.get("TIPO DE PARTICIPANTE"), "")) if resolved.get("TIPO DE PARTICIPANTE") else ""
        grupo = canon(row.get(resolved.get("GRUPO ETARIO INTERNO"), "")) if resolved.get("GRUPO ETARIO INTERNO") else ""
        if edad is not None:
            if edad < 0:
                add_error(errors, fila, pid, "EDAD DEL PARTICIPANTE", "Edad inválida", "CRÍTICO", "Coherencia", f"Edad negativa: {edad}.")
            if "NINO" in tipo or "NINA" in tipo or "ADOLESCENTE" in tipo or "JOVEN" in tipo:
                if edad >= 18:
                    add_error(errors, fila, pid, "TIPO DE PARTICIPANTE", "Incoherencia edad/tipo", "ALTO", "Coherencia", f"Registrado como NNAJ con edad {int(edad)}.")
            if "CUIDADOR" in tipo and edad < 18:
                add_error(errors, fila, pid, "TIPO DE PARTICIPANTE", "Incoherencia edad/tipo", "ALTO", "Coherencia", f"Registrado como cuidador con edad {int(edad)}.")
            expected_group = expected_group_from_age(edad)
            if grupo and expected_group and canon(expected_group) != grupo:
                add_error(errors, fila, pid, "GRUPO ETARIO INTERNO", "Grupo etario inconsistente", "ADVERTENCIA", "Coherencia",
                          f'Edad {int(edad)} sugiere "{expected_group}", pero figura "{literal(row.get(resolved.get("GRUPO ETARIO INTERNO"), ""))}".')

        # documento
        doc_type = row.get(doc_type_col, "") if doc_type_col else ""
        doc_num = row.get(doc_num_col, "") if doc_num_col else ""
        dt = literal(doc_type)
        dc = limpio_doc(doc_num)
        if dt:
            if dt in DOC_SIN_NUMERO:
                if dc:
                    add_error(errors, fila, pid, "NÚMERO DE DOCUMENTO DE IDENTIDAD DEL PARTICIPANTE", "Número innecesario", "ADVERTENCIA", "Coherencia",
                              f'El tipo "{dt}" no requiere número, pero tiene "{literal(doc_num)}".')
            else:
                if not dc:
                    add_error(errors, fila, pid, "NÚMERO DE DOCUMENTO DE IDENTIDAD DEL PARTICIPANTE", "Campo obligatorio vacío", "CRÍTICO", "Completud",
                              f'El tipo "{dt}" requiere número de documento.')
                else:
                    hom = None
                    for k in DOC_LONGITUDES:
                        if canon(k) == canon(dt):
                            hom = k
                            break
                    if hom:
                        mn, mx = DOC_LONGITUDES[hom]
                        lg = len(dc)
                        if not (mn <= lg <= mx):
                            add_error(errors, fila, pid, "NÚMERO DE DOCUMENTO DE IDENTIDAD DEL PARTICIPANTE", "Longitud de documento incorrecta", "ALTO", "Coherencia",
                                      f'El tipo "{dt}" espera {mn}-{mx} caracteres y tiene {lg}.')

        # departamento/municipio
        dep_raw = row.get(resolved.get("DEPARTAMENTO"), "") if resolved.get("DEPARTAMENTO") else ""
        mun_raw = row.get(resolved.get("MUNICIPIO"), "") if resolved.get("MUNICIPIO") else ""
        dep = canon(dep_raw)
        mun = canon(mun_raw)
        dep = dep.replace("LA GUAJIRA", "LA GUAJIRA")
        if dep in DEP_MUNI and mun and mun not in {canon(x) for x in DEP_MUNI[dep]}:
            add_error(errors, fila, pid, "MUNICIPIO", "Municipio no corresponde al departamento", "ALTO", "Coherencia",
                      f'Municipio "{literal(mun_raw)}" no pertenece a "{literal(dep_raw)}".')

        # estatus migratorio y nacionalidad
        nac = canon(row.get(resolved.get("NACIONALIDAD DEL PARTICIPANTE"), "")) if resolved.get("NACIONALIDAD DEL PARTICIPANTE") else ""
        est = canon(row.get(resolved.get("ESTATUS MIGRATORIO DEL PARTICIPANTE"), "")) if resolved.get("ESTATUS MIGRATORIO DEL PARTICIPANTE") else ""
        if nac == "COLOMBIANO/A" and est in {"IRREGULAR", "REGULAR"}:
            add_error(errors, fila, pid, "ESTATUS MIGRATORIO DEL PARTICIPANTE", "Estatus migratorio inconsistente", "ADVERTENCIA", "Coherencia",
                      "Para nacionalidad colombiana normalmente se espera NO APLICA.")

        # duplicados
        if pid:
            if pid in seen_ids:
                add_error(errors, fila, pid, "ID DEL PARTICIPANTE", "Duplicado", "ALTO", "Duplicidad",
                          f'ID duplicado. Primera aparición en fila {seen_ids[pid]}.')
            else:
                seen_ids[pid] = fila
        if dt and dc:
            key = canon(dt) + "|" + dc
            if key in seen_docs:
                add_error(errors, fila, pid, "DOCUMENTO", "Duplicado", "ALTO", "Duplicidad",
                          f'Documento duplicado. Primera aparición en fila {seen_docs[key]}.')
            else:
                seen_docs[key] = fila

    detail = pd.DataFrame(errors)
    crit = detail[detail["Severidad"].isin(["CRÍTICO", "ALTO"])].copy() if not detail.empty else pd.DataFrame()

    resumen_rows = []
    if not detail.empty:
        grouped = detail.groupby(["Tipo de error", "Severidad"]).size().reset_index(name="Cantidad")
        for _, r in grouped.iterrows():
            resumen_rows.append({"Tipo de problema": r["Tipo de error"], "Severidad": r["Severidad"], "Cantidad": int(r["Cantidad"])})
    resumen = pd.DataFrame(resumen_rows)
    homolog = pd.DataFrame({"Campo estándar": list(resolved.keys()), "Columna interpretada": list(resolved.values())})
    return {"RESUMEN": resumen, "DETALLE DE ERRORES": detail, "INCOHERENCIAS CRÍTICAS": crit, "HOMOLOGACIÓN DE COLUMNAS": homolog}


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("1450x820")
        self.configure(bg="#f0f2f5")
        self.results = None
        self.current_detail = pd.DataFrame()
        self._build()

    def _build(self):
        header = tk.Frame(self, bg="#1a1a2e", height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="🔎 Auditoría de Reporte Nacional", font=("Segoe UI", 15, "bold"), bg="#1a1a2e", fg="white").pack(side="left", padx=20, pady=14)

        top = tk.Frame(self, bg="#f0f2f5", pady=10)
        top.pack(fill="x", padx=20)
        tk.Button(top, text="📋 Pegar desde portapapeles", command=self.paste_clipboard, bg="#2980b9", fg="white", relief="flat", font=("Segoe UI", 10, "bold"), padx=12, pady=6).pack(side="left")
        tk.Button(top, text="🧹 Limpiar texto", command=self.clean_text, bg="#7f8c8d", fg="white", relief="flat", font=("Segoe UI", 10), padx=12, pady=6).pack(side="left", padx=8)
        tk.Button(top, text="▶ Analizar", command=self.run_analysis, bg="#27ae60", fg="white", relief="flat", font=("Segoe UI", 10, "bold"), padx=12, pady=6).pack(side="left")
        tk.Button(top, text="💾 Exportar resultados", command=self.export_results, bg="#8e44ad", fg="white", relief="flat", font=("Segoe UI", 10), padx=12, pady=6).pack(side="left", padx=8)

        middle = tk.PanedWindow(self, orient=tk.HORIZONTAL, sashrelief="raised", bg="#f0f2f5")
        middle.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        left = tk.Frame(middle, bg="#f0f2f5")
        right = tk.Frame(middle, bg="#f0f2f5")
        middle.add(left, minsize=420)
        middle.add(right, minsize=700)

        tk.Label(left, text="Pegue aquí la tabla copiada desde Excel", bg="#f0f2f5", font=("Segoe UI", 10, "bold")).pack(anchor="w")
        self.txt = tk.Text(left, wrap="none", font=("Consolas", 9), undo=True)
        y1 = ttk.Scrollbar(left, orient="vertical", command=self.txt.yview)
        x1 = ttk.Scrollbar(left, orient="horizontal", command=self.txt.xview)
        self.txt.configure(yscrollcommand=y1.set, xscrollcommand=x1.set)
        self.txt.pack(fill="both", expand=True, side="left")
        y1.pack(fill="y", side="right")
        x1.pack(fill="x", side="bottom")

        self.summary_frame = tk.Frame(right, bg="#f0f2f5")
        self.summary_frame.pack(fill="x", pady=(0, 8))

        filter_frame = tk.Frame(right, bg="#f0f2f5")
        filter_frame.pack(fill="x", pady=(0, 6))
        tk.Label(filter_frame, text="Filtrar por severidad:", bg="#f0f2f5", font=("Segoe UI", 9)).pack(side="left")
        self.var_filter = tk.StringVar(value="TODOS")
        for sev in ["TODOS", "CRÍTICO", "ALTO", "ADVERTENCIA", "INFO"]:
            fg = SEVERITY_COLORS.get(sev, "#333")
            tk.Radiobutton(filter_frame, text=sev, variable=self.var_filter, value=sev, bg="#f0f2f5", fg=fg,
                           selectcolor="#f0f2f5", command=self.refresh_table, font=("Segoe UI", 9, "bold")).pack(side="left", padx=6)
        tk.Label(filter_frame, text=" Buscar:", bg="#f0f2f5", font=("Segoe UI", 9)).pack(side="left", padx=(10, 2))
        self.var_search = tk.StringVar()
        self.var_search.trace_add("write", lambda *args: self.refresh_table())
        tk.Entry(filter_frame, textvariable=self.var_search, font=("Segoe UI", 9), width=30).pack(side="left")

        cols = ("Fila", "ID del Participante", "Columna", "Tipo de error", "Severidad", "Categoría", "Detalle")
        table_frame = tk.Frame(right, bg="#f0f2f5")
        table_frame.pack(fill="both", expand=True)
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings")
        widths = {"Fila": 60, "ID del Participante": 170, "Columna": 210, "Tipo de error": 180, "Severidad": 95, "Categoría": 110, "Detalle": 430}
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=widths[c], minwidth=50)
        ys = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        xs = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscroll=ys.set, xscroll=xs.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        ys.grid(row=0, column=1, sticky="ns")
        xs.grid(row=1, column=0, sticky="ew")
        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        self.status = tk.StringVar(value="Pegue la tabla del reporte nacional para iniciar.")
        tk.Label(self, textvariable=self.status, anchor="w", bg="#dde1e7", fg="#333", padx=10, font=("Segoe UI", 9)).pack(fill="x", side="bottom")

    def paste_clipboard(self):
        try:
            txt = self.clipboard_get()
            self.txt.delete("1.0", tk.END)
            self.txt.insert("1.0", txt)
            self.status.set("Contenido pegado desde portapapeles.")
        except Exception as e:
            messagebox.showerror("Error", f"No fue posible leer el portapapeles.\n{e}")

    def clean_text(self):
        raw = self.txt.get("1.0", tk.END)
        lines = [ln.replace("\ufeff", "") for ln in raw.splitlines() if normalize_spaces(ln)]
        lines = [ln for ln in lines if literal(ln) != "TOTAL GENERAL"]
        self.txt.delete("1.0", tk.END)
        self.txt.insert("1.0", "\n".join(lines))
        self.status.set("Texto limpiado.")

    def clear_summary(self):
        for w in self.summary_frame.winfo_children():
            w.destroy()

    def show_summary(self):
        self.clear_summary()
        if self.current_detail is None or self.current_detail.empty:
            tk.Label(self.summary_frame, text="✅ Sin hallazgos", font=("Segoe UI", 10, "bold"), bg="#d5f5e3", fg="#1e8449", padx=12, pady=6).pack(side="left")
            return
        counts = self.current_detail["Severidad"].value_counts()
        for sev in ["CRÍTICO", "ALTO", "ADVERTENCIA", "INFO"]:
            n = int(counts.get(sev, 0))
            if n == 0:
                continue
            bg = {"CRÍTICO": "#fdecea", "ALTO": "#fef3e2", "ADVERTENCIA": "#fffbea", "INFO": "#eaf4fb"}[sev]
            fr = tk.Frame(self.summary_frame, bg=bg, padx=10, pady=4)
            fr.pack(side="left", padx=4)
            tk.Label(fr, text=str(n), font=("Segoe UI", 14, "bold"), bg=bg, fg=SEVERITY_COLORS[sev]).pack()
            tk.Label(fr, text=sev, font=("Segoe UI", 8), bg=bg, fg=SEVERITY_COLORS[sev]).pack()

    def clear_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    def refresh_table(self):
        self.clear_table()
        if self.current_detail is None or self.current_detail.empty:
            return
        df = self.current_detail.copy()
        sev = self.var_filter.get()
        txt = self.var_search.get().strip().lower()
        if sev != "TODOS":
            df = df[df["Severidad"] == sev]
        if txt:
            mask = df.apply(lambda r: txt in " ".join(str(x).lower() for x in r.values), axis=1)
            df = df[mask]
        order = df["Severidad"].map(SEVERITY_ORDER).fillna(99)
        df = df.assign(_ord=order).sort_values(["_ord", "Fila"]).drop(columns=["_ord"])
        for _, r in df.iterrows():
            vals = tuple(r[c] if c in r.index else "" for c in self.tree["columns"])
            self.tree.insert("", "end", values=vals)

    def run_analysis(self):
        try:
            raw = self.txt.get("1.0", tk.END).strip()
            if not raw:
                messagebox.showwarning("Sin datos", "Pegue primero la tabla del reporte nacional.")
                return
            df = parse_clipboard(raw)
            self.results = audit_df(df)
            self.current_detail = self.results["DETALLE DE ERRORES"].copy() if not self.results["DETALLE DE ERRORES"].empty else pd.DataFrame()
            self.show_summary()
            self.refresh_table()
            self.status.set(f"Análisis completado. Filas analizadas: {len(df)}. Hallazgos: {len(self.current_detail)}.")
        except Exception as e:
            messagebox.showerror("Error en el análisis", str(e))
            self.status.set("No fue posible analizar la tabla.")

    def export_results(self):
        if not self.results:
            messagebox.showwarning("Sin resultados", "Primero ejecute el análisis.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel", "*.xlsx")], initialfile="Auditoria_Reporte_Nacional.xlsx")
        if not path:
            return
        try:
            with pd.ExcelWriter(path, engine="openpyxl") as writer:
                for name, out in self.results.items():
                    df_out = out.copy()
                    if df_out.empty:
                        df_out = pd.DataFrame({"Mensaje": ["Sin registros para esta hoja del reporte."]})
                    df_out.to_excel(writer, index=False, sheet_name=name[:31])
                raw = self.txt.get("1.0", tk.END).strip()
                if raw:
                    parse_clipboard(raw).to_excel(writer, index=False, sheet_name="TABLA PEGADA")
            messagebox.showinfo("Exportado", f"Reporte guardado en:\n{path}")
            self.status.set(f"Reporte exportado: {Path(path).name}")
        except Exception as e:
            messagebox.showerror("Error al exportar", str(e))


if __name__ == "__main__":
    app = App()
    app.mainloop()
