# Urutkan angka di dalam list, bisa secara menaik maupun menurun
dataList = [1, 4, 6, 7, 3, 2, 5, 8, 9] # data inputan

i = 0
while i < len(dataList) - 1:
    if dataList[i] > dataList[i+1]:
        temp = dataList[i]
        dataList[i] = dataList[i+1]
        dataList[i+1] = temp
        i = -1
    i += 1

print(f"Menaik : {dataList}")
print(f"Menurun : {dataList[::-1]}")

# Membuat setiap karakter pada string menjadi dua kali
string = "helow" # data inputan
output_text = ""

for i in range(len(string)):
    output_text += string[i] + string[i]

print(output_text)

# Convert angka integer ke teks, maksimal 9000000
def convertNumberToText(data):
    satuan = ["", "satu", "dua", "tiga", "empat", "lima", "enam", "tujuh", "delapan", "sembilan"]
    belasan = ["", "sebelas", "dua belas", "tiga belas", "empat belas", "lima belas", "enam belas", "tujuh belas", "delapan belas", "sembilan belas"]
    puluhan = ["", "sepuluh", "dua puluh", "tiga puluh", "empat puluh", "lima puluh", "enam puluh", "tujuh puluh", "delapan puluh", "sembilan puluh"]

    if data == 0:
        return "nol"
    elif data > 0 and data < 10:
        return satuan[data]
    elif data > 10 and data < 20:
        return belasan[data%10]
    elif data > 9 and data < 100 and not (data > 10 and data < 20):
        return puluhan[data//10] + " " + (satuan[data%10] if data%10 != 0 else "")
    elif data > 99 and data < 1000:
        return ("seratus" if data//100==1 else f"{satuan[data//100]} ratus") + " " + (convertNumberToText(data%100) if data%100 != 0 else "")
    elif data > 999 and data < 1000000:
        return ("seribu" if data//1000==1 else f"{convertNumberToText(data//1000)} ribu") + " " + (convertNumberToText(data%1000) if data%1000 != 0 else "")
    else:
        return convertNumberToText(data//1000000) + " " + "juta" + " " +(convertNumberToText(data % 1000000) if data % 1000000 != 0 else "")

# data inputan
number = 1213
print(convertNumberToText(number))