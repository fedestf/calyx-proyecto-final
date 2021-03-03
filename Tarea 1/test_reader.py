import tabula

tabula.convert_into("lista_precios.pdf", "output.tsv",
                    output_format="tsv", pages="all", area=[122, 49, 285, 559])
