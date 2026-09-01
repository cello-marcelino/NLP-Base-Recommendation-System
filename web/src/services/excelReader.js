import * as XLSX from 'xlsx'

export const parseLecturerExcel = (file) => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()

    reader.onload = (e) => {
      try {
        const data = new Uint8Array(e.target.result)
        const workbook = XLSX.read(data, { type: 'array' })
        const firstSheetName = workbook.SheetNames[0]
        const worksheet = workbook.Sheets[firstSheetName]
        const jsonRows = XLSX.utils.sheet_to_json(worksheet, { defval: '' })

        const formatValue = (row, possibleKeys) => {
          const keys = Object.keys(row)
          for (const key of keys) {
            const cleanKey = key.toLowerCase().trim()
            if (possibleKeys.includes(cleanKey)) {
              const val = row[key]
              return val !== undefined && val !== null ? String(val).trim() : ''
            }
          }
          return ''
        }

        const lecturerList = jsonRows.map((row) => {
          return {
            nidn: formatValue(row, ['nidn', 'id']),
            nama: formatValue(row, ['nama', 'nama dosen', 'nama lengkap']),
            program_studi: formatValue(row, ['program studi', 'prodi', 'program_studi']) || 'Teknik Informatika',
            bidang_keahlian: formatValue(row, ['bidang keahlian', 'keahlian', 'bidang_keahlian']),
            jurnal: formatValue(row, ['jurnal', 'publikasi', 'publikasi jurnal']),
            judul_bimbing: formatValue(row, ['judul bimbing', 'riwayat bimbingan', 'judul bimbingan', 'judul_bimbing']),
            judul_uji: formatValue(row, ['judul uji', 'riwayat pengujian', 'judul uji', 'judul_uji']),
            pendidikan: formatValue(row, ['pendidikan', 'riwayat pendidikan', 'pendidikan_terakhir'])
          }
        }).filter(d => d.nama)

        resolve(lecturerList)
      } catch (err) {
        reject(err)
      }
    }

    reader.onerror = (error) => reject(error)
    reader.readAsArrayBuffer(file)
  })
}
