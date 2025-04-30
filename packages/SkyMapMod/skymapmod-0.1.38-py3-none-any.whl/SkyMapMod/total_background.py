from astropy.coordinates import Galactic, ICRS, GeocentricMeanEcliptic, get_sun, get_body
from astropy.time import Time


from .zodiac import *
from .airglow import *
from .transparency import *
from .airglow_spectrum import *
from .modtran_default_kp_transparency import *
from .solar_spectrum import *
from .band_V_data import *
from .solar_radio_flux import *
from .star_catalogues import *
from .albedo_of_planets import *
from .planets import *

def galactic_to_equatorial(l, b):
    """
    Преобразует галактические координаты в эклиптические.

    Функция принимает галактическую долготу и широту объекта, преобразует их 
    в эклиптические координаты (долготу и широту) с использованием стандартной 
    эпохи J2000.0 и библиотеки `astropy`.

    Параметры:
        l (float): Галактическая долгота объекта (в градусах).
        b (float): Галактическая широта объекта (в градусах).

    Возвращает:
        tuple: Кортеж из двух значений:
            - ecl_lon (float): Эклиптическая долгота объекта (в градусах).
            - ecl_lat (float): Эклиптическая широта объекта (в градусах).

    Примечания:
        - Для преобразования используется библиотека `astropy`:
            - `Galactic`: Представляет галактические координаты.
            - `GeocentricMeanEcliptic`: Представляет эклиптические координаты.
        - Эпоха расчетов фиксирована как J2000.0.
        - Результат возвращается в градусах, так как это наиболее распространенный формат для астрономических данных.

    Зависимости:
        - `astropy.units`: Для работы с единицами измерения (градусы).
        - `astropy.time.Time`: Для задания эпохи J2000.0.
        - `astropy.coordinates.Galactic`: Для представления галактических координат.
        - `astropy.coordinates.GeocentricMeanEcliptic`: Для представления эклиптических координат.
    """
    import astropy.units as u
# Входные данные: галактические координаты и эпоха
    galactic_l = l * u.deg  # Галактическая долгота
    galactic_b = b * u.deg # Галактическая широта
    epoch = Time('J2000.0')  # Эпоха (стандартная для астрономических расчетов)

    # Создаем объект галактических координат
    galactic_coords = Galactic(l=galactic_l, b=galactic_b)

    # Преобразуем галактические координаты в экваториальные (ICRS)
    ecliptic_coords = galactic_coords.transform_to(GeocentricMeanEcliptic(equinox=epoch))


    print("Техническая проверка")
    print(f"Эклиптическая долгота (λ): {ecliptic_coords.lon.to(u.deg)}")
    print(f"Эклиптическая широта (β): {ecliptic_coords.lat.to(u.deg)}")
    
    ecl_lon = ecliptic_coords.lon.to(u.deg).value
    ecl_lat = ecliptic_coords.lat.to(u.deg).value
    return(ecl_lon, ecl_lat)

def Sun_ecl_lon(date, time):
    """
    Вычисляет эклиптическую долготу Солнца по заданным дате и времени.

    Функция принимает дату и время наблюдения, использует библиотеку `astropy` 
    для расчета положения Солнца в геоцентрической эклиптической системе координат 
    и возвращает эклиптическую долготу Солнца.

    Параметры:
        date (str): Дата наблюдения в формате 'YYYY-MM-DD' (например, '2023-11-03').
        time (str): Время наблюдения в формате 'HH:MM:SS' (например, '12:00:00').

    Возвращает:
        ecl_lon_of_Sun (float): Эклиптическая долгота Солнца (в градусах).

    Примечания:
        - Для расчетов используется библиотека `astropy`:
            - `get_sun`: Получает положение Солнца в геоцентрической системе координат.
            - `GeocentricMeanEcliptic`: Преобразует координаты в эклиптическую систему.
        - Результат возвращается в градусах, так как это наиболее распространенный формат 
          для астрономических данных.
        - Эклиптическая широта Солнца не возвращается, так как она не используется в дальнейших расчетах.

    Зависимости:
        - `astropy.time.Time`: Для обработки даты и времени.
        - `astropy.coordinates.get_sun`: Для получения положения Солнца.
        - `astropy.coordinates.GeocentricMeanEcliptic`: Для преобразования координат 
          в эклиптическую систему.
    """
    datetime = date + ' ' + time
    observation_time = Time(datetime)

    # Получаем координаты Солнца в геоцентрической системе координат
    sun_position = get_sun(observation_time)

    # Преобразуем координаты Солнца в эклиптическую систему (геоцентрическую)
    ecliptic_coords = sun_position.transform_to(GeocentricMeanEcliptic())

    # Извлекаем эклиптическую долготу (lon) и широту (lat)
    ecliptic_longitude = ecliptic_coords.lon
    ecliptic_latitude = ecliptic_coords.lat

    # Выводим результат
    print("Техническая проверка:")
    print(f"Эклиптическая долгота Солнца: {ecliptic_longitude}")
    print(f"Эклиптическая широта Солнца: {ecliptic_latitude}")
    ecl_lon_of_Sun = ecliptic_longitude.value
    return(ecl_lon_of_Sun)

def sum_of_spectrums(array_1, meaning_1, array_2, meaning_2):
    array = []
    meaning = []
    for i in range(array_1.shape[0]):
        for j in range(array_2.shape[0]):
            if array_1[i] == array_2[j]:
                array.append(array_1[i])
                meaning.append(meaning_1[i] + meaning_2[j])
    return np.array(array), np.array(meaning)


#собираем за атмосферой все 4 компоненты
#принимает на вход галактические координаты
#принимает на вход дату и время наблюдения по UTC
def total_background(l, b, date, time, Sun_sp_wl = wavelenght_newguey2003, Sun_sp_fx = flux_newguey2003, V_wl = wavelenght_band_V, V_tr = trancparency_band_V, wavelenght_airglow = wavelenght_kp, intensity_airglow = intensity_kp, wavelenght_atmosphere = wavelenght_modtran_kp, transparency_atmosphere = trancparency_modtran_kp, venus_albedo_wl = venus_alb_wl, venus_albedo_rf = venus_alb_rf, mars_albedo_wl = mars_alb_wl, mars_albedo_rf = mars_alb_rf, jupiter_albedo_wl = jupiter_alb_wl, jupiter_albedo_rf = jupiter_alb_rf, saturn_albedo_wl = saturn_alb_wl, saturn_albedo_rf = saturn_alb_rf):
    #получаем эклиптическую долготу Солнца
    lmbd_Sun = Sun_ecl_lon(date, time)
    #переводим галактические координаты в эклиптические геоцентрические
    lmbd, beta = galactic_to_equatorial(l, b)
    #получаем спектр зодиакального света (нм, фот / (м^2 сек нм ср))
    zodiac_wl, zodiac_spec = zodiacal_spectrum(lmbd, beta, lmbd_Sun, Sun_sp_wl, Sun_sp_fx, V_wl, V_tr)
    print('ФОТОНОВ ЗОДИКА:', integral(zodiac_wl, zodiac_spec))
#     return(zodiac_wl, zodiac_spec)

    #собственное свечение достаем
    airglow_wl, airglow_spec = airglow_spectrum(wavelenght_airglow, intensity_airglow, wavelenght_atmosphere, transparency_atmosphere)
    print('ФОТОНОВ СОБСТВЕННОГО:', integral(airglow_wl, airglow_spec))

#     return(airglow_wl, airglow_spec)
    #зод. свет и собств. свечение -- окей. Нужно допилить звездные каталоги и планеты.
    
    #звездные каталоги
    star_cat_wl = zodiac_wl
    star_cat_spec = star_spectrum(l, b, star_cat_wl)
    print('ФОТОНОВ ЗВЕЗД:', integral(star_cat_wl, star_cat_spec))
#     return star_cat_wl, star_cat_spec

    #планеты
    #Венера
    venus_l, venus_b = coordinates_of_planet('venus', date, time)
    print('Техническая проверка координат Венеры:', round(venus_l, 1), round(venus_b, 1))
    if round(venus_l, 1) == l and round(venus_b, 1) == b:
        venus_wl, venus_sp = venus_spectrum(date, time, Sun_sp_wl, Sun_sp_fx, venus_albedo_wl, venus_albedo_rf, V_wl, V_tr)
    else:
        venus_wl = zodiac_wl
        venus_sp = np.zeros(venus_wl.shape[0])
    print('ФОТОНОВ ВЕНЕРЫ:', integral(venus_wl, venus_sp))
    
    #Марс
    mars_l, mars_b = coordinates_of_planet('mars', date, time)
    print('Техническая проверка координат Марса:', round(mars_l, 1), round(mars_b, 1))
    if round(mars_l, 1) == l and round(mars_b, 1) == b:
        mars_wl, mars_sp = mars_spectrum(date, time, Sun_sp_wl, Sun_sp_fx, mars_albedo_wl, mars_albedo_rf, V_wl, V_tr)
    else:
        mars_wl = zodiac_wl
        mars_sp = np.zeros(mars_wl.shape[0])
    print('ФОТОНОВ МАРСА:', integral(mars_wl, mars_sp))
        
    #Юпитер
    jupiter_l, jupiter_b = coordinates_of_planet('jupiter', date, time)
    print('Техническая проверка координат Юпитера:', round(jupiter_l, 1), round(jupiter_b, 1))
    if round(jupiter_l, 1) == l and round(jupiter_b, 1) == b:
        jupiter_wl, jupiter_sp = jupiter_spectrum(date, time, Sun_sp_wl, Sun_sp_fx, jupiter_albedo_wl, jupiter_albedo_rf, V_wl, V_tr)
    else:
        jupiter_wl = zodiac_wl
        jupiter_sp = np.zeros(jupiter_wl.shape[0])
    print('ФОТОНОВ ЮПИТЕРА:', integral(jupiter_wl, jupiter_sp))
        
    #Сатурн
    saturn_l, saturn_b = coordinates_of_planet('saturn', date, time)
    print('Техническая проверка координат Сатурна:', round(saturn_l, 1), round(saturn_b, 1))
    if round(saturn_l, 1) == l and round(saturn_b, 1) == b:
        saturn_wl, saturn_sp = saturn_spectrum(date, time, Sun_sp_wl, Sun_sp_fx, saturn_albedo_wl, saturn_albedo_rf, V_wl, V_tr)
    else:
        saturn_wl = zodiac_wl
        saturn_sp = np.zeros(saturn_wl.shape[0])
    print('ФОТОНОВ САТУРНА:', integral(saturn_wl, saturn_sp))
        
    #теперь бы объединить эти спектры
    #делаю на основе функции sum_of_spectrums
    zod_air_wl, zod_air_sp = sum_of_spectrums(zodiac_wl, zodiac_spec, airglow_wl, airglow_spec)
    
    z_a_s_wl, z_a_s_sp = sum_of_spectrums(zod_air_wl, zod_air_sp, star_cat_wl, star_cat_spec)
    
    zas_v_wl, zas_v_sp = sum_of_spectrums(z_a_s_wl, z_a_s_sp, venus_wl, venus_sp)
    zas_vm_wl, zas_vm_sp = sum_of_spectrums(zas_v_wl, zas_v_sp, mars_wl, mars_sp)
    zas_vmj_wl, zas_vmj_sp = sum_of_spectrums(zas_vm_wl, zas_vm_sp, jupiter_wl, jupiter_sp)
    zas_vmjs_wl, zas_vmjs_sp = sum_of_spectrums(zas_vmj_wl, zas_vmj_sp, saturn_wl, saturn_sp)
    
    return zas_vmjs_wl, zas_vmjs_sp