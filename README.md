# PortScanner

## Açıklama
`PortScanner`, girilen IP adreslerinde belirtilen portların durumunu hızlı bir şekilde kontrol eden basit fakat esnek bir araçtır.

## Özellikler
- `Tek bir IP adresi veya ağ bloğu için tarama`
- `Argparse tabanlı komut satırı arayüzü`
- `Çoklu iş parçacığı ile hızlı tarama ve iş parçacığı sayısını ayarlayabilme`
- `Virgül ve aralık tabanlı esnek port seçimi (ör. 22,80,8000-8100)`
- `Sonuçları JSON dosyasına kaydedebilme`

## Kurulum
`Bu depoyu klonlayın veya indirin.`

```bash
git clone https://github.com/akportscanner/port-scan.py
cd PortScanner
```

Python 3.x sürümüne sahip olduğunuzdan emin olun.


### Kullanım
```bash
python3 port-scan.py -t 192.168.1.0/24 -p 22,80,8000-8100 -w 50 -o sonuc.json
```
Parametreler:
- `-t / --target` : Tarama yapılacak tek bir IP adresi veya ağ bloğu.
- `-p / --ports`  : Virgüller ve aralıklarla belirtilecek port listesi.
- `-w / --workers`: İsteğe bağlı iş parçacığı (thread) sayısı. Varsayılan **100**.
- `-o / --output` : Sonuçların yazılacağı JSON dosyası.

```Uyarı```
PortScanner'ı yalnızca kendi sistemlerinizde veya açıkça izin verilen sistemlerde kullanın. İzinsiz bir şekilde başka bir bilgisayarda port taraması yapmak yasa dışıdır ve etik olmayan bir davranıştır.


# PortScanner Güncelleme Notları

Bu sürümde PortScanner'a bazı önemli özellikler ve geliştirmeler ekledik.

## Yenilikler ve Değişiklikler

1. **Servis Tespiti**: 
    - PortScanner artık bir portta çalışan yaygın bir servisin adını da tespit edebiliyor.
    ```python
    def get_service(port):
        """Port numarasına göre yaygın servis adını döndürür."""
        service_name = socket.getservbyport(port, 'tcp')
        return service_name or 'Unknown'
    ```

2. **İlerleme Bilgilendirmesi**:
    - Kullanıcının hangi IP'nin tarandığını ve toplam IP sayısı içerisindeki sırasını görebilmesi için ilerleme bilgilendirmesi ekledik.
    ```python
    for index, ip in enumerate(all_ips, 1):
        print(f"{index}/{len(all_ips)} - {ip} taranıyor...")
    ```

3. **Daha Açıklayıcı Çıktılar**:
    - Açık portlar listelenirken, sadece port numarası yerine, port numarasıyla birlikte çalışan servisi de gösteriyoruz.
    ```python
    port_strings = [f"{port} ({service})" for port, service in open_ports]
    print(f"{ip} üzerindeki açık portlar: {', '.join(port_strings)}")
    ```

4. **Hata Yönetimi**:
    - Potansiyel hataları yakalayabilmek için geniş bir `except` bloğu kullandık. İleride bu hataların daha spesifik bir şekilde yönetilmesi planlanıyor.
