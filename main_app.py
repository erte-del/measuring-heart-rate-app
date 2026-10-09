from kivy.app import App  # Kivy uygulamasını oluşturmak için temel sınıfı içe aktarır.
from kivy.uix.screenmanager import ScreenManager, Screen  # Ekranlar arasında geçiş yapmayı sağlar.
from kivy.uix.boxlayout import BoxLayout  # Widget'ları dikey veya yatay olarak düzenlemek için kullanılır.
from kivy.uix.label import Label  # Kullanıcıya metin göstermek için etiket widget'ı.
from kivy.uix.button import Button  # Kullanıcının tıklayabileceği buton widget'ı.
from kivy.uix.textinput import TextInput  # Kullanıcının veri girebileceği metin giriş alanı.
from kivy.core.window import Window  # Pencere özelliklerini değiştirmek için kullanılır.
from kivy.uix.scrollview import ScrollView  # Kaydırılabilir bir görünüm oluşturmak için kullanılır.


from instructions import txt_instruction, txt_test1, txt_test2, txt_test3, txt_sits  # Talimat metinlerini içe aktarır.
from ruffier import test  # Ruffier testinin hesaplanmasını sağlayan fonksiyonu içe aktarır.


from seconds import Seconds  # Geri sayım için özel bir zamanlayıcı sınıfı.
from sits import Sits  # Oturma testindeki tekrarları sayan sınıf.
from runner import Runner  # Oturma testi sırasında hareketleri yöneten sınıf.


Window.clearcolor = (.87, 0.54, 0.8, 0.3)  # Uygulamanın arka plan rengini belirler (RGBA formatında).
btn_color = (0.98, 0.31, 0.8, 1)  # Butonların rengini belirleyen RGBA renk kodu.


age = 7  # Varsayılan yaş değeri.
name = ""  # Kullanıcının adını saklamak için boş bir string.
p1, p2, p3 = 0, 0, 0  # Kalp atış hızı değerlerini tutan değişkenler.


def check_int(str_num):  # Kullanıcının girdiği değerin tam sayı olup olmadığını kontrol eden fonksiyon.
   try:
       return int(str_num)  # Eğer dönüşüm başarılı olursa tam sayı olarak döndür.
   except:
       return False  # Hata oluşursa False döndür.






class InstrScr(Screen):  # InstrScr sınıfını tanımlar, bu sınıf Screen'den türetilmiştir.
   def __init__(self, **kwargs):  # Ekranı başlatırken gerekli argümanları alır
       super().__init__(**kwargs)  # Screen sınıfının __init__ metodunu çağırır


       instr = Label(text=txt_instruction)  # Kullanıcıya talimat verecek bir etiket oluşturur
       lbl1 = Label(text='Please enter your name:', halign='right')  # İsmin girileceği etiket
       self.in_name = TextInput(multiline=False)  # İsmin girileceği bir TextInput nesnesi
       lbl2 = Label(text='Please enter your age:', halign='right')  # Yaşın girileceği etiket
       self.in_age = TextInput(text='7', multiline=False)  # Yaşın girileceği TextInput, varsayılan değer 7


       self.btn = Button(text='Start', size_hint=(0.3, 0.2), pos_hint={'center_x': 0.5})  # 'Başla' butonunu oluşturur
       self.btn.background_color = btn_color  # Butonun arka plan rengini ayarlar
       self.btn.on_press = self.next  # Butona tıklanıldığında 'next' fonksiyonunu çalıştırır


       line1 = BoxLayout(size_hint=(0.8, None), height='30sp')  # İlk giriş için bir BoxLayout oluşturur
       line2 = BoxLayout(size_hint=(0.8, None), height='30sp')  # İkinci giriş için bir BoxLayout oluşturur
       line1.add_widget(lbl1)  # İlk etiketini ilk satıra ekler
       line1.add_widget(self.in_name)  # İsmin girişi için olan TextInput'u ilk satıra ekler
       line2.add_widget(lbl2)  # İkinci etiketini ikinci satıra ekler
       line2.add_widget(self.in_age)  # Yaşın girişi için olan TextInput'u ikinci satıra ekler


       outer = BoxLayout(orientation='vertical', padding=8, spacing=8)  # Dış düzen (BoxLayout) oluşturur
       outer.add_widget(instr)  # Talimat etiketini dış düzene ekler
       outer.add_widget(line1)  # İlk satırı dış düzene ekler
       outer.add_widget(line2)  # İkinci satırı dış düzene ekler
       outer.add_widget(self.btn)  # Başla butonunu dış düzene ekler
       self.add_widget(outer)  # Dış düzeni ekrana ekler


   def next(self):  # Butona basıldığında çalışacak fonksiyon
       name = self.in_name.text  # Kullanıcının girdiği ismi alır
       age = check_int(self.in_age.text)  # Yaşı alır ve bir tam sayıya dönüştürür (check_int fonksiyonu ile)
       if age == False or age < 7:  # Eğer yaş geçersizse veya 7'den küçükse
           age = 7  # Yaş değeri 7 olarak ayarlanır
           self.in_age.text = str(age)  # Yaş giriş alanını 7 ile günceller
       else:
           self.manager.current = 'nabız1'  # 'nabız1' ekranına geçiş yapılır


class PulseScr(Screen):  # PulseScr sınıfını tanımla, bu bir Screen (Ekran) türüdür
   def __init__(self, **kwargs):  # Ekranı verilen argümanlarla başlat
       super().__init__(**kwargs)  # Üst sınıfın __init__ metodunu çağır
       self.next_screen = False  # Sonraki ekranın gösterilip gösterilemeyeceğini takip eden değişken
  
       instr = Label(text=txt_test1)  # Talimatları görüntülemek için bir etiket oluştur
       self.lbl_sec = Seconds(15)  # 15 saniyelik bir sayaç (zamanlayıcı) oluştur
       self.lbl_sec.bind(done=self.sec_finished)  # 'done' olayı tamamlandığında sec_finished fonksiyonunu çağır


       line = BoxLayout(size_hint=(0.8, None), height='30sp')  # Giriş alanları için bir BoxLayout oluştur
       lbl_result = Label(text='Please enter your result:', halign='right')  # Sonuç girişi isteyen etiket
       self.in_result = TextInput(text='0', multiline=False)  # Sonuç için giriş alanı (varsayılan '0')
       self.in_result.set_disabled(True)  # Başlangıçta giriş alanını devre dışı bırak
  
       line.add_widget(lbl_result)  # Sonuç etiketini düzen içine ekle
       line.add_widget(self.in_result)  # Sonuç giriş alanını düzen içine ekle
       self.btn = Button(text='Start', size_hint=(0.3, 0.4), pos_hint={'center_x': 0.5})  # 'Başla' butonu oluştur
       self.btn.background_color = btn_color  # Butonun arka plan rengini ayarla
       self.btn.on_press = self.next  # Butona basıldığında next fonksiyonunu çağır
       outer = BoxLayout(orientation='vertical', padding=8, spacing=8)  # Tüm öğeleri içeren dış düzeni oluştur
       outer.add_widget(instr)  # Talimat etiketini dış düzen içine ekle
       #outer.add_widget(lbl1)  # (Yorum satırında) Gerekirse başka bir etiket ekle
       outer.add_widget(self.lbl_sec)  # Sayaç etiketini dış düzen içine ekle
       outer.add_widget(line)  # Sonuç giriş alanlarını dış düzen içine ekle
       outer.add_widget(self.btn)  # Başlatma butonunu dış düzen içine ekle
       self.add_widget(outer)  # Dış düzeni ekrana ekle


   def sec_finished(self, *args):  # Sayaç tamamlandığında çağrılan fonksiyon
       self.next_screen = True  # Sonraki ekrana geçişin mümkün olduğunu belirten bayrak değişkeni
       self.in_result.set_disabled(False)  # Sonuç giriş alanını etkinleştir
       self.btn.set_disabled(False)  # Butonu etkinleştir
       self.btn.text = 'Continue'  # Buton metnini 'Devam Et' olarak değiştir


   def next(self):  # Butona basıldığında çağrılan fonksiyon
       if not self.next_screen:  # Eğer sayaç tamamlanmadıysa
           self.btn.set_disabled(True)  # Butonu devre dışı bırak, çoklu basılmayı önle
           self.lbl_sec.start()  # Sayaç başlat
       else:  # Eğer sayaç tamamlandıysa
           global p1  # p1 değişkenini global olarak tanımla
           p1 = check_int(self.in_result.text)  # Giriş değerini check_int fonksiyonu ile tamsayıya çevir
           if p1 == False or p1 <= 0:  # Eğer giriş değeri geçersiz veya 0'dan küçük/eşitse
               p1 = 0  # p1'i 0 olarak ayarla
               self.in_result.text = str(p1)  # Sonuç giriş alanını güncelle
           else:
               self.manager.current = 'oturma_tekrarları'  # Geçerli bir giriş varsa 'oturma_tekrarları' ekranına geç


class CheckSits(Screen):  # CheckSits sınıfını tanımlar, bu sınıf Screen'den türetilmiştir.
   def __init__(self, **kwargs):  # Ekranı başlatırken gerekli argümanları alır
       super().__init__(**kwargs)  # Screen sınıfının __init__ metodunu çağırır
       self.next_screen = False  # Sonraki ekranın gösterilip gösterilmeyeceğini belirten değişken


       instr = Label(text=txt_sits, size_hint=(0.5, 1))  # Egzersizle ilgili talimatları içeren etiket
       self.lbl_sits = Sits(30)  # 30 tekrardan oluşan bir Sits nesnesi oluşturur
       self.run = Runner(total=30, steptime=1.5, size_hint=(0.4, 1))  # 30 adım, her adımda 1.5 saniye süreyle bir Runner nesnesi oluşturur
       self.run.bind(finished=self.run_finished)  # 'finished' olayını run_finished fonksiyonuna bağlar


       line = BoxLayout()  # Bileşenleri yatay olarak yerleştirmek için bir BoxLayout oluşturur
       vlay = BoxLayout(orientation='vertical', size_hint=(0.3, 1))  # Dikey düzen için başka bir BoxLayout oluşturur
       vlay.add_widget(self.lbl_sits)  # Sits nesnesini dikey düzenine ekler
       line.add_widget(instr)  # Talimat etiketini yatay düzenine ekler
       line.add_widget(vlay)  # Dikey düzeni yatay düzene ekler
       line.add_widget(self.run)  # Runner nesnesini yatay düzenine ekler


       self.btn = Button(text='Start', size_hint=(0.3, 0.2), pos_hint={'center_x': 0.5})  # Başlatma butonu oluşturur
       self.btn.background_color = btn_color  # Butonun arka plan rengini ayarlar
       self.btn.on_press = self.next  # Butona tıklanıldığında 'next' fonksiyonunu çalıştırır


       outer = BoxLayout(orientation='vertical', padding=8, spacing=8)  # Tüm bileşenleri barındıracak dış bir düzen oluşturur
       outer.add_widget(line)  # Yatay düzeni dış düzenine ekler
       outer.add_widget(self.btn)  # Başlatma butonunu dış düzenine ekler


       self.add_widget(outer)  # Dış düzeni ekrana ekler
  
   def run_finished(self, instance, value):  # Runner tamamlandığında çağrılacak fonksiyon
       self.btn.set_disabled(False)  # Butonu etkinleştirir
       self.btn.text = 'Continue'  # Buton metnini 'Devam Et' olarak değiştirir
       self.next_screen = True  # Sonraki ekranın gösterilebileceği bayrağını True yapar


   def next(self):  # Butona basıldığında çalışacak fonksiyon
       if not self.next_screen:  # Eğer sonraki ekran henüz gösterilemiyorsa
           self.btn.set_disabled(True)  # Butonu devre dışı bırakır
           self.run.start()  # Egzersizi başlatır
           self.run.bind(value=self.lbl_sits.next)  # 'value' olayıyla Sits nesnesinin sayacını günceller
       else:  # Eğer sonraki ekran gösterilmeye hazırsa
           self.manager.current = 'nabız2'  # 'nabız2' ekranına geçiş yapar


class PulseScr2(Screen):  # PulseScr2 sınıfını tanımlar, bu sınıf Screen'den türetilmiştir.
   def __init__(self, **kwargs):  # Ekranı başlatırken gerekli argümanları alır
       self.next_screen = False  # Sonraki ekranın gösterilip gösterilmeyeceğini belirten değişken
       self.stage = 0  # Sürecin hangi aşamasında olduğumuzu izleyen değişken


       super().__init__(**kwargs)  # Screen sınıfının __init__ metodunu çağırır


       instr = Label(text=txt_test3)  # Testin talimatlarını içeren etiket
       line1 = BoxLayout(size_hint=(0.8, None), height='30sp')  # İlk sonuç girişi için düzen
       self.lbl_sec = Seconds(15)  # 15 saniyelik bir zamanlayıcı oluşturur
       self.lbl_sec.bind(done=self.sec_finished)  # 'done' olayı tamamlandığında sec_finished fonksiyonunu çalıştırır
       self.lbl1 = Label(text='Mesure your heart rate.')  # Şu anki talimatı göstermek için etiket


       lbl_result1 = Label(text='Sonuç:', halign='right')  # İlk sonuç için etiket
       self.in_result1 = TextInput(text='0', multiline=False)  # İlk sonucu girecek kullanıcıdan alacak input alanı
       line1.add_widget(lbl_result1)  # İlk etiketi ilk satıra ekler
       line1.add_widget(self.in_result1)  # İlk sonuç input'unu ilk satıra ekler


       line2 = BoxLayout(size_hint=(0.8, None), height='30sp')  # İkinci sonuç girişi için düzen
       lbl_result2 = Label(text='Result after resting:', halign='right')  # İkinci sonuç için etiket
       self.in_result2 = TextInput(text='0', multiline=False)  # İkinci sonucu girecek input alanı


       # Başlangıçta her iki sonuç input alanını devre dışı bırakır
       self.in_result1.set_disabled(True)
       self.in_result2.set_disabled(True)


       line2.add_widget(lbl_result2)  # İkinci etiketi ikinci satıra ekler
       line2.add_widget(self.in_result2)  # İkinci sonuç input'unu ikinci satıra ekler


       self.btn = Button(text='Start', size_hint=(0.3, 0.5), pos_hint={'center_x': 0.5})  # Başlatma butonu
       self.btn.background_color = btn_color  # Butonun arka plan rengini ayarlar
       self.btn.on_press = self.next  # Butona tıklandığında 'next' fonksiyonunu çalıştırır


       # Tüm bileşenleri dış bir düzen (outer) içine yerleştirir
       outer = BoxLayout(orientation='vertical', padding=8, spacing=8)
       outer.add_widget(instr)  # Talimat etiketini dış düzenine ekler
       outer.add_widget(self.lbl1)  # İlk talimat etiketini dış düzenine ekler
       outer.add_widget(self.lbl_sec)  # Zamanlayıcı etiketini dış düzenine ekler
       outer.add_widget(line1)  # İlk sonuç satırını dış düzenine ekler
       outer.add_widget(line2)  # İkinci sonuç satırını dış düzenine ekler
       outer.add_widget(self.btn)  # Başlatma butonunu dış düzenine ekler


       self.add_widget(outer)  # Dış düzeni ekrana ekler


   def sec_finished(self, *args):  # Zamanlayıcı bitince çalışacak fonksiyon
       if self.lbl_sec.done == True:  # Eğer zamanlayıcı tamamlandıysa
           if self.stage == 0:  # İlk aşama (nabız ölçümü)
               self.stage = 1  # İkinci aşamaya geçiş yapar (dinlenme)
               self.lbl1.text = 'Resting time'  # Talimat metnini değiştirir
               self.lbl_sec.restart(30)  # 30 saniyelik bir dinlenme zamanlayıcısını başlatır
               self.in_result1.set_disabled(False)  # İlk sonuç input'unu etkinleştirir
           elif self.stage == 1:  # İkinci aşama (dinlenme)
               self.stage = 2  # Üçüncü aşamaya geçiş yapar (nabız hesaplaması)
               self.lbl1.text = 'Mesure your heart rate.'  # Talimat metnini değiştirir
               self.lbl_sec.restart(15)  # 15 saniyelik hesaplama zamanlayıcısını başlatır
           elif self.stage == 2:  # Üçüncü aşama (sonuç girişi sonrası)
               self.in_result2.set_disabled(False)  # İkinci sonuç input'unu etkinleştirir
               self.btn.set_disabled(False)  # Butonu etkinleştirir
               self.btn.text = 'End'  # Butonun metnini 'End' olarak değiştirir
               self.next_screen = True  # Sonraki ekranı göstermek için bayrağı True yapar


   def next(self):  # Butona basıldığında çalışacak fonksiyon
       if not self.next_screen:  # Eğer sonraki ekran henüz ulaşılabilir değilse
           self.btn.set_disabled(True)  # Butonu devre dışı bırakır
           self.lbl_sec.start()  # Zamanlayıcıyı başlatır
       else:  # Eğer sonraki ekran gösterilebilir durumda ise
           global p2, p3  # p2 ve p3 değişkenlerini global olarak tanımlar
           p2 = check_int(self.in_result1.text)  # İlk sonucu tamsayıya çevirir
           p3 = check_int(self.in_result2.text)  # İkinci sonucu tamsayıya çevirir


           # Eğer ilk sonuç geçerli değilse, değeri 0 yapar
           if p2 == False:
               p2 = 0
               self.in_result1.text = str(p2)


           # Eğer ikinci sonuç geçerli değilse, değeri 0 yapar
           elif p3 == False:
               p3 = 0
               self.in_result2.text = str(p3)


           else:
               # Sonuç ekranına geçiş yapar
               self.manager.current = 'Result'






class Result(Screen):
   def __init__(self, **kwargs):
       super().__init__(**kwargs)  # Screen sınıfının __init__ metodunu çağırarak ekranı başlatır.
       self.outer = BoxLayout(orientation='vertical', padding=8, spacing=8)  # Dikey düzeni (BoxLayout) tanımlar.
       self.instr = Label(text = '')  # Boş bir etiket oluşturur.
       self.outer.add_widget(self.instr)  # Bu etiketi dış düzenin içine ekler.
       self.add_widget(self.outer)  # Dış düzeni (BoxLayout) ekranın içine ekler.
       self.on_enter = self.before  # Ekran açıldığında before metodunun çalıştırılmasını sağlar.
      
   def before(self):
       global name  # 'name' değişkenini global olarak kullanır.
       self.instr.text = name + '\n' + test(p1, p2, p3, age)  # 'name' ve 'test' fonksiyonunun çıktısını etikete ekler.
class HeartCheck(App):
   def build(self):
       sm = ScreenManager()  # Ekranlar arasında geçiş yapabilmek için ScreenManager oluşturur.
       sm.add_widget(InstrScr(name='instr'))  # İlk ekran olan InstrScr'i ekler.
       sm.add_widget(PulseScr(name='nabız1'))  # İkinci ekran olan PulseScr'i ekler.
       sm.add_widget(CheckSits(name='oturma_tekrarları'))  # Üçüncü ekran olan CheckSits'i ekler.
       sm.add_widget(PulseScr2(name='nabız2'))  # Dördüncü ekran olan PulseScr2'yi ekler.
       sm.add_widget(Result(name='sonuç'))  # Son ekran olan Result'ı ekler.
       return sm  # ScreenManager'ı geri döner, böylece ekranlar arasında geçiş yapılabilir.


app = HeartCheck()  # HeartCheck sınıfından bir nesne oluşturur.
app.run()  # Uygulamayı çalıştırır.





