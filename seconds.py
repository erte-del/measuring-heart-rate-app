from kivy.uix.label import Label  # Kivy'den Label bileşenini içe aktarıyoruz.
from kivy.clock import Clock  # Zamanlayıcı işlemleri için Clock modülünü içe aktarıyoruz.
from kivy.properties import BooleanProperty  # BooleanProperty ile bir özellik tanımlıyoruz.


class Seconds(Label):  # Label sınıfından türetilmiş bir Seconds sınıfı oluşturuyoruz.
  done = BooleanProperty(False)  # done adında, başlangıçta False olan bir boolean özellik tanımlıyoruz.


  def __init__(self, total, **kwargs):
      self.done = False  # Sayaç henüz tamamlanmadığı için done değişkenini False yapıyoruz.
      self.current = 0  # Geçen süreyi 0 olarak başlatıyoruz.
      self.total = total  # Sayaç için belirlenen toplam süreci (kaç saniye sayılacağını) saklıyoruz.
      my_text = "Geçen saniye: " + str(self.current)  # Başlangıç metnini oluşturuyoruz.
      super().__init__(text=my_text)  # Label bileşenine bu başlangıç metnini iletiyoruz.


  def restart(self, total, **kwargs):
      self.done = False  # Sayaç sıfırlandığında tekrar False yapıyoruz.
      self.total = total  # Yeni toplam süreyi güncelliyoruz.
      self.current = 0  # Sayacı sıfırlıyoruz.
      self.text = "Geçen saniye: " + str(self.current)  # Ekrandaki metni sıfırdan başlatıyoruz.
      self.start()  # Yeni süre ile sayacı başlatıyoruz.


  def start(self):
      Clock.schedule_interval(self.change, 1)  # Her 1 saniyede bir 'change' metodunu çağırarak sayacı başlatıyoruz.


  def change(self, dt):
      self.current += 1  # Sayaç değerini bir arttırıyoruz.
      self.text = "Geçen saniye: " + str(self.current)  # Güncellenmiş değeri ekranda gösteriyoruz.
      if self.current >= self.total:  # Eğer sayaç belirlenen toplam süreye ulaşırsa:
          self.done = True  # done özelliğini True yapıyoruz (sayacın tamamlandığını gösteriyoruz).
          return False  # Clock.schedule_interval çağrısını iptal ederek zamanlayıcıyı durduruyoruz.

