import csv
import os
from models import PermintaanLayanan

KOLOM_WAJIB = {
    "id_mahasiswa", "nama", "nim", "jenis_layanan",
    "prioritas", "waktu_kedatangan", "estimasi_waktu_layanan",
}


def load_dataset_csv(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"File dataset tidak ditemukan: '{path}'")

    dataset = []
    error_list = []

    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        if not KOLOM_WAJIB.issubset(set(reader.fieldnames or [])):
            raise ValueError(
                f"Format CSV tidak sesuai. Kolom wajib: {sorted(KOLOM_WAJIB)}"
            )

        nim_terlihat = set()
        for nomor_baris, row in enumerate(reader, start=2):  # baris 1 = header
            try:
                nim = str(row["nim"]).strip()
                if nim in nim_terlihat:
                    error_list.append(
                        (nomor_baris, f"NIM {nim} duplikat di dalam file, baris dilewati")
                    )
                    continue

                item = PermintaanLayanan(
                    id_mahasiswa=row["id_mahasiswa"],
                    nama=row["nama"],
                    nim=nim,
                    jenis_layanan=row["jenis_layanan"],
                    prioritas=row["prioritas"],
                    waktu_kedatangan=row["waktu_kedatangan"],
                    estimasi_waktu_layanan=row["estimasi_waktu_layanan"],
                )
                dataset.append(item)
                nim_terlihat.add(nim)
            except (ValueError, KeyError) as e:
                error_list.append((nomor_baris, str(e)))

    return dataset, error_list


def save_dataset_csv(dataset, path):
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)

    fieldnames = ["id_mahasiswa", "nama", "nim", "jenis_layanan",
                  "prioritas", "waktu_kedatangan", "estimasi_waktu_layanan"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for item in dataset:
            writer.writerow(item.to_dict())
