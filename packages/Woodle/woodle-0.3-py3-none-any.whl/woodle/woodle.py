import csv
import optparse
import os
import sys
import shutil
from tempfile import NamedTemporaryFile

import pandas as pd


class FichierManquant(IOError):
    def __init__(self, message, filename):
        super().__init__(2, message, filename)


class ColonneIntrouvable(KeyError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


def convert(input_file, output_file, col, bareme):
    if not os.path.exists(input_file):
        raise FichierManquant("le fichier n'existe pas", input_file)
    if not os.path.exists(output_file):
        raise FichierManquant("le fichier n'existe pas", output_file)
    if input_file.endswith(".csv"):
        donnees_promo = pd.read_csv(input_file, sep=",")
    else:
        try:
            donnees_promo = pd.read_excel(input_file).set_index("Numéro d'identification")
        except KeyError:
            donnees_promo = pd.read_excel(input_file).set_index("Numéro d’identification")

    try:
        notes = donnees_promo[col]
    except KeyError:
        raise ColonneIntrouvable(col)

    tempfile = NamedTemporaryFile(mode="w+", encoding="iso-8859-1", delete=False)

    with open(output_file, "r", encoding="iso-8859-1") as csvFile, tempfile:
        reader = csv.reader(csvFile, delimiter=";", quotechar='"')
        writer = csv.writer(tempfile, delimiter=";", quotechar='"')

        for row in reader:
            try:
                code = int(row[0])
                note = notes[code]
                if note != "-":
                    row[4] = note
                    row[5] = bareme
            except (IndexError, ValueError):
                pass
            except KeyError:
                print(
                    f"Attention : étudiant n°{code} ({row[1]} {row[2].capitalize()}) non présent dans le fichier de notes."
                )
                pass
            writer.writerow(row)

    shutil.move(tempfile.name, output_file)


def main():
    """
    Point d'entrée pour le traitement.

    :return: codes de sortie standards.
    """
    # noinspection SpellCheckingInspection
    usage = "usage: %prog [option] <fichier moodle> <fichier snw> <colonne>"
    parser = optparse.OptionParser(usage=usage, add_help_option=False)
    parser.add_option("-b", dest="bareme", help="Barème.", metavar="BAREME", default=20)
    parser.add_option(
        "-h", "--help", action="help", help="Affiche ce message d'aide et termine."
    )
    (opt, args) = parser.parse_args()
    if len(args) != 3:
        parser.error("Mauvais nombre de paramètres.")

    input_file = args[0]
    output_file = args[1]
    col = args[2]

    try:
        float(opt.bareme)
        if not float(opt.bareme).is_integer():
            raise ValueError
        b = int(opt.bareme)
    except ValueError:
        print(f"Erreur : {opt.bareme} n'est pas un nombre entier", file=sys.stderr)
        sys.exit(1)
    try:
        convert(input_file, output_file, col, b)

    except FichierManquant as e:
        print(f"Erreur : {e.strerror} ({e.filename})", file=sys.stderr)
        sys.exit(1)
    except ColonneIntrouvable as e:
        print(f"Erreur : la colonne {e.args[0]} n'existe pas.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
