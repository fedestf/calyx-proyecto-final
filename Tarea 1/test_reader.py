import tabula

tabula.convert_into(r"Tarea 1\lista_precios.pdf", "output.tsv",
                    output_format="tsv", pages=1, area=[122, 49, 285, 559])
