# ДЗ 1. Расчёт A/B-теста для рекомендательных тегов
from statistics import NormalDist
# данные из задания
dau = 5_000_000        # пользователей в день
searches = 4           # поисков на пользователя в день
tagged = 0.6           # доля поисков с тегами
p0 = 0.030             # CTR сейчас
p1 = 0.033             # CTR с эффектом +10%
alpha = 0.05
power = 0.8

# пусть доля подходящих запросов (6%)
suitable = 0.06

# 1. сколько поисков нужно на группу (если поиски независимы)
norm = NormalDist()
z = norm.inv_cdf(1 - alpha / 2) + norm.inv_cdf(power)
n = z ** 2 * (p0 * (1 - p0) + p1 * (1 - p1)) / (p1 - p0) ** 2
print("Поисков на группу без поправки:", round(n))

# 2. поправка на то, что поиски одного пользователя похожи
def calc(days, rho):
    m = searches * tagged * suitable * days # подходящих поисков на пользователя
    de = max(1, 1 + (m - 1) * rho)          # дизайн-эффект
    n_group = n * de                        # поисков на группу
    users = 2 * n_group / m                 # пользователей на обе группы
    return m, de, n_group, users
print()
for days in (7, 14):
    m, de, n_group, users = calc(days, 0.05)
    print(days, "дней: m =", round(m, 2), ", DE =", round(de, 2),
          ", поисков на группу =", round(n_group),
          ", пользователей =", round(users),
          "(", round(users / dau * 100, 2), "% )")

# 3. 2% пользователей, 14 дней
share = 0.02
days = 14
users = dau * share
m = searches * tagged * suitable * days
have = users / 2 * m
need = calc(14, 0.05)[2]
print()
print("Выбрали:", share * 100, "% пользователей,", days, "дней")
print("Пользователей в тесте:", round(users), ", в группе:", round(users / 2))
print("Подходящих поисков на группу:", round(have), ", нужно:", round(need))

# 4. если подходящих запросов меньше 6%
print()
print("Если подходящих запросов меньше:")
for s in (0.03, 0.04, 0.05, 0.06):
    suitable = s
    users = calc(14, 0.05)[3]
    print(round(s * 100), "% запросов: нужно", round(users / dau * 100, 2), "% пользователей")

input("\nНажми Enter, чтобы закрыть окно")