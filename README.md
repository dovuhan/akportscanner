# PortScanner

## Açıklama
`PortScanner`, belirtilen bir IP adresine veya IP aralığındaki belirtilen portlarda hangi portların açık olduğunu kontrol eden basit ve etkili bir araçtır.

## Özellikler
- `Tek bir IP adresi veya IP aralığı için port taraması.`
- `Hızlı tarama için çoklu iş parçacığı desteği.`
- `Esnek port aralığı seçimi.`

## Kurulum
`Bu depoyu klonlayın veya indirin.`

```bash
git clone https://github.com/akportscanner/port-scan.py
cd PortScanner
```

Python 3.x sürümüne sahip olduğunuzdan emin olun.


```bash Kullanım
bash 
Copy code
python3 port-scan.py
Bu komutu çalıştırdıktan sonra, taramak istediğiniz IP adresini/aralığını ve port aralığını girmeniz istenecektir.
```

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
