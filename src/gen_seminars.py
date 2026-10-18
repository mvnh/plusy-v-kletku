#!/usr/bin/env python3
"""Seminar questions -> data/predict.json. Answers for 'out' are computed by running clang natively
unless given explicitly; given answers are checked against the run (except UB/CE/platform-dependent)."""
import json, os, subprocess, tempfile, sys, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import ROOT, TMP, CXX
SCR = TMP
HEAD = """#include <iostream>
#include <iomanip>
#include <string>
#include <string_view>
#include <cstdint>
#include <climits>
#include <cmath>
#include <cstring>
#include <memory>
#include <utility>
#include <limits>
"""
def full_code(q):
    c = q['code'].strip('\n')
    if q.get('wrap') == 'main':
        inc, body = [], []
        for l in c.split('\n'): (inc if l.lstrip().startswith('#') else body).append(l)
        return HEAD + '\n'.join(inc) + '\nint main() {\n' + '\n'.join('    ' + l for l in body) + '\n    return 0;\n}\n'
    if q.get('wrap') == 'inc':
        return HEAD + c + '\n'
    return c + '\n'
def run(code, stdin=''):
    d = tempfile.mkdtemp(dir=SCR); src = os.path.join(d, 'm.cpp'); open(src, 'w').write(code)
    c = subprocess.run([CXX, '-std=c++20', '-w', src, '-o', os.path.join(d, 'a')], capture_output=True, text=True)
    if c.returncode: return 'CE', c.stderr
    r = subprocess.run([os.path.join(d, 'a')], input=stdin, capture_output=True, text=True, timeout=5)
    return r.returncode, r.stdout
def norm(s): return '\n'.join(l.rstrip() for l in s.split('\n')).rstrip('\n')

Q = []
def add(sem, n, ch, q, code=None, type='out', **kw):
    Q.append(dict(sem=sem, n=n, ch=ch, q=q, code=code, type=type, **kw))

# ---------------- Семинар 1 ----------------
add(1, '1.1', '01', 'Какие из строк — корректные идентификаторы C++?', type='multi',
    opts=['<code>my_var</code>', '<code>_count</code>', '<code>2fast</code>', '<code>for</code>', '<code>user-name</code>', '<code>User_Name</code>'], ans=[0, 1, 5],
    why='<code>2fast</code> начинается с цифры, <code>for</code> — ключевое слово, <code>user-name</code> содержит минус (это выражение «user минус name»).')
add(1, '1.2', '02', 'Определи тип литерала <code>42LL</code>.', type='single',
    opts=['int', 'long', 'long long', 'unsigned long long'], ans=2,
    why='Суффиксы: <code>42</code> — int, <code>42U</code> — unsigned int, <code>42L</code> — long, <code>42LL</code> — long long, <code>3.14</code> — double, <code>3.14f</code> — float, <code>\'A\'</code> — char, <code>"A"</code> — const char[2] (строковый литерал: символ плюс терминал).')
add(1, '1.2б', '02', 'А какой тип у литерала <code>"A"</code>?', type='single',
    opts=['char', 'const char[2]', 'std::string', 'const char[1]'], ans=1,
    why='Строковый литерал — массив <code>const char</code> длиной «символы + 1» под терминал <code>\'\\0\'</code>.')
add(1, '1.3', '02', 'Определи результат выражения.', '''#include <iostream>
int main() {
    std::cout << ((5 > 3) && (2 == 0));
}''', why='<code>5 &gt; 3</code> — true, <code>2 == 0</code> — false, true && false = false → печатается <b>0</b>. Короткая логика: если бы левая часть была false, правую даже не вычисляли бы.')
add(1, '1.4', '02', 'Объясни разницу между <code>&amp;</code> и <code>&amp;&amp;</code>, <code>|</code> и <code>||</code>. Приведи примеры.', type='open',
    why='<code>&amp;</code> и <code>|</code> — <b>побитовые</b> операции: работают с каждым битом и всегда вычисляют оба операнда (<code>5 &amp; 3 == 1</code>, <code>5 | 3 == 7</code>). <code>&amp;&amp;</code> и <code>||</code> — <b>логические</b>: работают с bool, результат true/false, и они <b>ленивые</b> — правый операнд не вычисляется, если результат ясен по левому (<code>p != nullptr &amp;&amp; *p &gt; 0</code> безопасно). Пример разницы: <code>2 &amp; 1 == 0</code>, но <code>2 &amp;&amp; 1 == true</code>.')
add(1, '1.5', '02', 'Какой тип имеет результат выражения <code>\'a\' + 1</code>?', type='single',
    opts=['char', 'int', 'unsigned char', 'зависит от компилятора'], ans=1,
    why='При арифметике всё, что меньше <code>int</code>, сначала повышается до <code>int</code> (integral promotion). Поэтому <code>std::cout &lt;&lt; \'a\' + 1</code> печатает 98, а не «b».')
add(1, '1.6', '01', 'Чему равен <code>x</code>? Поясни порядок вычислений.', '''#include <iostream>
int main() {
    int x = 5 + 3 * 2 - 4 / 2;
    std::cout << x;
}''', why='Сначала умножение и деление (приоритет выше): 3·2 = 6, 4/2 = 2. Потом слева направо: 5 + 6 − 2 = <b>9</b>.')
add(1, '1.7', '03', 'Рассмотри код и объясни результат. (Подумай, корректен ли он вообще.)', '''#include <iostream>

int main() {
    int a = 0;
    std::cout << a << ' ' << a++ << a << '\\n';
    std::cout << a << ' ' << ++a << a << '\\n';
    std::cout << a << ' ' << a-- << a << '\\n';
    std::cout << a << ' ' << --a << a << '\\n';
    return 0;
}''', type='single', opts=['0 01 / 1 22 / 2 21 / 1 00 — всё строго определено', 'Неопределённое/неуточнённое поведение: порядок вычисления операндов нельзя предсказать', 'Ошибка компиляции'], ans=1, ub=True,
    why='В конспекте это помечено как UB: одна переменная меняется и читается в одном выражении. Формально с C++17 операнды <code>&lt;&lt;</code> вычисляются слева направо, и вывод будет 0 01, 1 22, 2 21, 1 00. Но старые компиляторы и стандарты дают другое, а главное правило не меняется: <b>не меняй переменную несколько раз в одном выражении</b>, разноси по строкам. Помни: <code>a++</code> возвращает старое значение, <code>++a</code> — новое.')
add(1, '1.8', '03', 'Что выведет программа?', '''#include <iostream>

int main() {
    int a = 0;
    std::cout << (a++ + ++a);
    return 0;
}''', ans=['UB'], ub=True,
    why='Две модификации <code>a</code> в одном выражении без упорядочивания, а у операндов <code>+</code> порядок вычисления не определён → <b>UB</b>. clang обычно печатает 2 и выдаёт предупреждение <code>multiple unsequenced modifications</code>, но полагаться на это нельзя.')
add(1, '1.9', '03', 'Чему равно значение <code>y</code> после выполнения кода?', '''int main() {
    int x = 5;
    int y = (x = 10) + (x = 20);
    return y;
}''', type='text', ans=['UB'], ub=True, ph='число или UB',
    why='Два присваивания одной переменной в операндах <code>+</code> не упорядочены → <b>UB</b>. Компиляторы выдают кто 30, кто 40.')
add(1, '1.10', '07', 'Что выведет программа?', '''#include <iostream>

int main() {
    unsigned char x = 255;
    x++;
    std::cout << (int)x << "\\n";
    return 0;
}''', why='<code>unsigned char</code>: 255 + 1 по модулю 256 = <b>0</b>. Это законное переполнение беззнакового.')
add(1, '1.11', '07', 'Что произойдёт при сложении больших чисел? Почему?', '''#include <iostream>

int main() {
    int a = 1000000000; // 1 миллиард
    int b = 2000000000; // 2 миллиарда
    int c = a + b;
    std::cout << c;
    return 0;
}''', ans=['UB'], ub=True,
    why='3 000 000 000 больше <code>INT_MAX</code> (2 147 483 647). Переполнение знакового — <b>UB</b>. На практике железо «прокрутит» значение и напечатает −1294967296, но компилятор вправе сделать что угодно. Лечится <code>long long</code>.')
add(1, '1.12', '07', 'Что из этого — UB? (<code>int a = INT_MAX; a++;</code> / <code>int b = -1; b &gt;&gt; 1;</code> / <code>int c = 5 / 0;</code>)', type='multi',
    opts=['<code>a++</code> при <code>a = INT_MAX</code>', '<code>-1 &gt;&gt; 1</code>', '<code>5 / 0</code>'], ans=[0, 2],
    why='Переполнение знакового и целочисленное деление на ноль — UB. Сдвиг вправо отрицательного по конспекту implementation-defined (зависит от реализации), а с C++20 он гарантированно арифметический: <code>-1 &gt;&gt; 1 == -1</code>.')
add(1, '1.13', '02', 'Какой будет результат? Почему?', '''#include <iostream>

int main() {
    int a = 20, b = 50;
    std::cout << a / b << '\\n';
    return 0;
}''', why='Оба операнда <code>int</code> → целочисленное деление, 0.4 отбрасывается до <b>0</b>.')
add(1, '1.14', '03', 'Что выведет программа?', '''#include <iostream>

int main() {
    int a = 5;
    int b = (a *= 2, a + 3);
    std::cout << "a=" << a << ", b=" << b;
    return 0;
}''', why='Запятая: сначала <code>a *= 2</code> (a = 10), потом результат — правый операнд <code>a + 3</code> = 13.')
add(1, '1.15', '03', 'Что выведет программа и с каким кодом она завершится? Введи вывод.', '''#include <iostream>
int main() {
    int a = 1, b = 2, c = 3;
    int x = (a++, b++, c++);
    std::cout << a << b << c;
    int y = (a, b, c);
    return (x = 5, y = 10, x + y);
}''', why='Все три инкремента выполнятся по порядку, <code>x</code> получит значение последнего операнда — старое <code>c</code>, то есть 3. Вывод: <b>234</b>. <code>y = c = 4</code>. Код возврата: <code>(x = 5, y = 10, x + y)</code> = 15.')

# ---------------- Семинар 2 ----------------
add(2, '2.1', '02', 'Что выведет программа?', '''#include <iostream>
int main() {
    std::cout << 11 / 4 << '\\n';
}''', why='Целочисленное деление: 2.75 → <b>2</b>.')
add(2, '2.2', '02', 'Что выведет программа?', '''#include <iostream>
int main() {
    std::cout << 11.0 / 4 << '\\n';
}''', why='Один операнд <code>double</code> → вещественное деление: <b>2.75</b>.')
add(2, '2.3', '02', 'Что выведет программа?', '''#include <iostream>
int main() {
    int a = 0;
    bool b = true || (++a > 0);
    std::cout << a << '\\n';
}''', why='Слева <code>true</code> — результат <code>||</code> уже известен, правая часть не вычисляется. <code>a</code> остаётся <b>0</b>.')
add(2, '2.4', '02', 'Что выведет программа?', '''#include <iostream>
int main() {
    int a = 0;
    bool b = false && (++a > 0);
    std::cout << a << '\\n';
}''', why='Слева <code>false</code> — <code>&amp;&amp;</code> правую часть не считает: <b>0</b>.')
add(2, '2.5', '05', 'Что выведет программа?', '''#include <iostream>
int main() {
    unsigned short a = 6, b = 3;
    std::cout << (a & b) << " " << (a | b) << " " << (a ^ b) << '\\n';
}''', why='6 = 110, 3 = 011. AND = 010 = 2, OR = 111 = 7, XOR = 101 = 5.')
add(2, '2.6', '05', 'Что выведет программа?', '''#include <iostream>
int main() {
    unsigned short a = 3;
    std::cout << (a << 3) << " " << (a >> 1) << '\\n';
}''', why='3 · 2³ = 24; 3 / 2 = 1.')
add(2, '2.7', '05', 'Что выведет программа?', '''#include <iostream>
int main() {
    short a = -8;
    std::cout << (a >> 1) << '\\n';
}''', why='Арифметический сдвиг сохраняет знак: −8 / 2 = <b>−4</b>. По конспекту поведение implementation-defined, но все популярные компиляторы (и стандарт с C++20) делают арифметический сдвиг.')
add(2, '2.8', '02', 'Что выведет программа (на 64-битном Linux/macOS)?', '''#include <iostream>
int main() {
    std::cout << sizeof(0) << " " << sizeof(0L) << " " << sizeof(0LL) << '\\n';
}''', ans=['4 8 8', '4 4 8'], plat=True,
    why='<code>int</code> — 4, <code>long</code> — 8 на 64-битных Linux/macOS (но 4 на Windows), <code>long long</code> — 8. Засчитываются оба варианта.')
add(2, '2.9', '02', 'Что выведет программа? Подумай о типах результатов.', '''#include <iostream>
int main() {
    std::cout << (0u + 0) << " " << (0ul + 0ll) << '\\n';
}''', why='Значения нули: <b>0 0</b>. Интереснее типы: <code>0u + 0</code> — unsigned int, <code>0ul + 0ll</code> — unsigned long long или long long в зависимости от платформы.')
add(2, '2.10', '06', 'Что выведет программа?', '''#include <iostream>
int main() {
    double a = 0.1, b = 0.2;
    std::cout.setf(std::ios::fixed);
    std::cout.precision(17);
    std::cout << (a + b) << '\\n';
}''', why='17 знаков после запятой показывают ошибку представления: 0.1 и 0.2 неточны в двоичной системе.')
add(2, '2.11', '06', 'Что выведет программа?', '''#include <iostream>
int main() {
    double x = 1.0/0.0;
    double y = 0.0/0.0;
    std::cout << (x > 0) << " " << (x == x) << " " << (y == y) << '\\n';
}''', why='<code>x = +inf</code>: больше нуля и равен себе. <code>y = NaN</code>, а NaN <b>не равен ничему, даже себе</b>: <code>y == y</code> — false. На этом основан классический тест на NaN: <code>x != x</code>.')
add(2, '2.12', '05', 'Что выведет программа?', '''#include <iostream>
int main() {
    unsigned int a = 12, b = 5;
    std::cout << (a & b) << " " << (a | b) << " " << (a ^ b) << '\\n';
}''', why='12 = 1100, 5 = 0101: AND = 0100 = 4, OR = 1101 = 13, XOR = 1001 = 9.')
add(2, '2.13', '05', 'Что выведет программа (unsigned int — 32 бита)?', '''#include <iostream>
int main() {
    unsigned int x = 7;
    std::cout << ~x << '\\n';
}''', why='~7 = 2³² − 1 − 7 = <b>4294967288</b>. Результат зависит от размера <code>unsigned int</code>.')
add(2, '2.14', '05', 'Что выведет программа?', '''#include <iostream>
int main() {
    unsigned int x = 3;
    std::cout << (x << 2) << '\\n';
}''', why='Сдвиг влево на 2 — умножение на 4: <b>12</b>.')
add(2, '2.15', '05', 'Что выведет программа?', '''#include <iostream>
int main() {
    unsigned int x = 32;
    std::cout << (x >> 3) << '\\n';
}''', why='Сдвиг вправо на 3 — деление на 8: <b>4</b>.')
add(2, '2.16', '05', 'Что выведет программа?', '''#include <iostream>
int main() {
    unsigned int x = 5;
    std::cout << ((x << 1) + (x >> 1)) << '\\n';
}''', why='10 + 2 = <b>12</b>.')
add(2, '2.17', '05', 'Что выведет программа?', '''#include <iostream>
int main() {
    unsigned int a = 42;
    std::cout << (a ^ a) << '\\n';
}''', why='a ⊕ a = 0 для любого a.')
add(2, '2.18', '05', 'Что выведет программа?', '''#include <iostream>
int main() {
    unsigned int a = 7, b = 12;
    a = a ^ b;
    b = a ^ b;
    a = a ^ b;
    std::cout << a << " " << b << '\\n';
}''', why='Обмен через XOR: значения поменялись местами — <b>12 7</b>.')
add(2, '2.19', '05', 'Что выведет программа?', '''#include <iostream>
int main() {
    unsigned int mask = 1 << 3; // 8
    unsigned int x = 13;
    std::cout << (x & mask) << '\\n';
}''', why='13 = 1101, бит 3 установлен → результат <b>8</b> (не 1! AND возвращает маску, а не bool).')
add(2, '2.20', '05', 'Что выведет программа?', '''#include <iostream>
int main() {
    unsigned int x = 5;
    unsigned int mask = 1 << 2;
    std::cout << (x | mask) << '\\n';
}''', why='5 = 101, бит 2 уже установлен → <b>5</b>.')
add(2, '2.21', '05', 'Что выведет программа?', '''#include <iostream>
int main() {
    unsigned int x = 13;
    unsigned int mask = ~(1 << 2);
    std::cout << (x & mask) << '\\n';
}''', why='Сбрасываем бит 2 у 1101 → 1001 = <b>9</b>.')
add(2, '2.22', '05', 'Что выведет программа?', '''#include <iostream>
int main() {
    unsigned int x = 9;
    unsigned int mask = 1 << 3;
    std::cout << (x ^ mask) << '\\n';
}''', why='Переключаем бит 3 у 1001 → 0001 = <b>1</b>.')
add(2, '2.23', '05', 'Что выведет программа?', '''#include <iostream>
int main() {
    unsigned int x = 57;
    std::cout << (x & 1) << '\\n';
}''', why='Младший бит — признак нечётности: 57 нечётное → <b>1</b>.')
add(2, '2.24', '05', 'Что выведет программа?', '''#include <iostream>
int main() {
    unsigned int x = 11;
    std::cout << (x << 1) << '\\n';
}''', why='11 · 2 = <b>22</b>.')
add(2, '2.25', '05', 'Что выведет программа?', '''#include <iostream>
int main() {
    unsigned int x = 25;
    std::cout << (x >> 1) << '\\n';
}''', why='25 / 2 = <b>12</b> (целочисленно).')
add(2, '2.26', '05', 'Что выведет программа? И что вычисляет эта формула?', '''#include <iostream>
int main() {
    unsigned int x = 6;
    unsigned int y = 10;
    std::cout << ((x & y) << 1) + (x | y) << '\\n';
}''', why='<code>x &amp; y</code> = 0110 &amp; 1010 = 0010 = 2, сдвиг даёт 4; <code>x | y</code> = 1110 = 14; итого <b>18</b>. Скобки вокруг сдвига обязательны, а <code>+</code> связывается раньше, чем <code>&lt;&lt;</code> потока. Что вычисляет формула: известно, что <code>x + y == (x | y) + (x &amp; y)</code>, поэтому здесь получается <code>x + y + (x &amp; y)</code> = 16 + 2.')

# ---------------- Семинар 3 ----------------
add(3, '3.1', '08', 'Какой тип у результата выражения <code>true ? 1 : 2.5</code>?', type='single', opts=['int', 'double', 'float', 'bool'], ans=1,
    why='Тип условной операции — общий тип операндов, он не зависит от условия: <code>int</code> и <code>double</code> → <code>double</code>. Значение будет 1.0.')
add(3, '3.2', '08', 'Какое утверждение про <code>if</code> с инициализацией верно?', type='single',
    opts=['Переменная из init живёт до конца программы', 'Переменная обязана быть константой', 'init может содержать только объявление переменной', 'Область видимости переменной ограничена оператором if (включая else)'], ans=3,
    why='Переменная из init видна в условии и во всех ветках, включая <code>else</code>, и умирает после оператора. init может быть и выражением, константой быть не обязана.')
add(3, '3.3', '08', 'Какие типы могут использоваться в условии <code>switch</code>?', type='single',
    opts=['Только int', 'Любые целые типы, char, enum', 'Любые целые типы', 'int, float, double'], ans=1,
    why='Целые и перечислимые типы (а <code>char</code> — тоже целый). Вещественные и строки — нельзя.')
add(3, '3.4', '09', 'Какой порядок выполнения частей цикла <code>for</code>?', type='single',
    opts=['init → condition → statement → expression', 'init → statement → condition → expression', 'condition → init → statement → expression', 'statement → init → condition → expression'], ans=0,
    why='init один раз, затем по кругу: проверка условия → тело → expression → проверка…')
add(3, '3.5', '09', 'Как ведёт себя <code>continue</code> в цикле <code>for</code>?', type='single',
    opts=['Прерывает цикл полностью', 'Переходит к проверке условия, пропуская expression', 'Переходит к expression, затем к проверке условия', 'Возвращает управление в начало функции'], ans=2,
    why='В <code>for</code> после <code>continue</code> выполняется expression (например, <code>++i</code>), потом условие. В <code>while</code> — сразу условие.')
add(3, '3.6', '08', 'Что выведет программа?', '''#include <iostream>

int main() {
    int x = -3;
    if (x) std::cout << "nonzero\\n";
    if (!x) std::cout << "zero\\n";
}''', why='Любое ненулевое значение (в том числе отрицательное) — true.')
add(3, '3.7', '08', 'Что выведет программа?', '''#include <iostream>

int main() {
    int x = 0;
    if (int y = x + 5; y > 3) {
        std::cout << y << '\\n';
    }
}''', why='init создаёт <code>y = 5</code>, условие 5 &gt; 3 истинно → <b>5</b>.')
add(3, '3.8', '08', 'Что выведет программа?', '''#include <iostream>

int main() {
    if (true)
    if (false) std::cout << "A\\n";
    else std::cout << "B\\n";
}''', why='<code>else</code> относится к ближайшему <code>if (false)</code> → <b>B</b>.')
add(3, '3.9', '08', 'Что выведет программа?', '''#include <iostream>

int main() {
    int a = 2, b = 5, c = 3;
    if (a >= b) {
        if (a >= c) std::cout << a << '\\n';
        else std::cout << c << '\\n';
    } else if (b >= c) {
        std::cout << b << '\\n';
    } else {
        std::cout << c << '\\n';
    }
}''', why='Максимум из трёх: 2 &lt; 5, 5 ≥ 3 → <b>5</b>.')
add(3, '3.10', '08', 'Что выведет программа? Есть ли здесь ошибка?', '''#include <iostream>

int main() {
    int x = 0;
    if (x);
}''', type='single', opts=['Ничего не выведет, код корректен (if с пустым оператором)', 'Ошибка компиляции из-за ;', 'UB', 'Выведет 0'], ans=0,
    why='<code>;</code> — пустой оператор, законное тело <code>if</code>. Программа ничего не делает. Компилятор может предупредить: обычно это опечатка.')
add(3, '3.11', '08', 'Что выведет программа?', '''#include <iostream>

int main() {
    int x = 1, y = 2, z = 3;
    if (const int t = y + z; t != 5)
        std::cout << t << '\\n';
}''', ans=[''], why='<code>t = 5</code>, условие <code>t != 5</code> ложно — <b>ничего</b> не выводится (оставь поле пустым).')
add(3, '3.12', '08', 'Что выведет программа при вводе 5, 0 и −3 (три запуска)? Запиши три ответа через пробел.', '''#include <iostream>

int main() {
    int x;
    std::cin >> x;
    if (x > 0) std::cout << "positive\\n";
    else if (x == 0) std::cout << "zero\\n";
    else std::cout << "negative\\n";
}''', type='text', ans=['positive zero negative'], stdin='5', why='Классическая цепочка <code>else if</code>.')
add(3, '3.13', '08', 'Что выведет программа?', '''#include <iostream>

int main() {
    int x = 5, y = 0;
    if (x = y) std::cout << "Equal\\n";
    else std::cout << "Not equal\\n";
}''', why='Ловушка: <code>=</code> вместо <code>==</code>! <code>x = y</code> присваивает 0 и возвращает 0 → false → <b>Not equal</b>. Компилятор предупреждает о присваивании в условии.')
add(3, '3.14', '08', 'Что выведет программа?', '''#include <iostream>

int main() {
    int a = 4, b = 7;
    std::cout << (a > b ? a - b : b - a) << '\\n';
}''', why='Модуль разности: 7 − 4 = <b>3</b>.')
add(3, '3.15', '08', 'Что выведет программа?', '''#include <iostream>

int main() {
    int x = 0;
    if (x++ > 0) std::cout << "A\\n";
    else if (++x > 1) std::cout << "B\\n";
    else std::cout << "C\\n";
}''', why='<code>x++ &gt; 0</code>: сравнивается старое 0 → false, x = 1. Затем <code>++x &gt; 1</code>: x = 2, 2 &gt; 1 → <b>B</b>.')
add(3, '3.16', '09', 'Что выведет программа?', '''#include <iostream>

int main() {
    int i = 0;
    for (;;) {
        if (i == 3) break;
        std::cout << i++;
    }
    std::cout << '\\n';
}''', why='Бесконечный <code>for</code> с выходом по <code>break</code>: печатает 0, 1, 2 подряд → <b>012</b>.')
add(3, '3.17', '09', 'Что выведет программа?', '''#include <iostream>

int main() {
    for (int i = 0; i < 4; ++i) {
        for (int j = 0; j < 4; ++j) {
            if (j == 1) continue;
            if (i == 2) break;
            std::cout << i << j << ' ';
        }
    }
    std::cout << '\\n';
}''', why='<code>j = 1</code> всегда пропускается через <code>continue</code>. При <code>i = 2</code> уже на первой итерации (j = 0) срабатывает <code>break</code>, но он выходит <b>только из внутреннего</b> цикла, поэтому строка для <code>i = 3</code> снова печатается.')

# ---------------- Семинар 4 ----------------
add(4, '4.1', '10', 'Что выведет фрагмент?', '''int ownMax(int x, int y) { return x > y ? x : y; }
int main() {
    std::cout << ownMax(3, 5) << '\\n';
}''', wrap='inc', why='Максимум из 3 и 5.')
add(4, '4.2', '10', 'Что выведет фрагмент?', '''int f(int x = 10) { return x; }
int main() {
    std::cout << f() << ' ' << f(20) << '\\n';
}''', wrap='inc', why='Без аргумента берётся значение по умолчанию 10.')
add(4, '4.3', '10', 'Что выведет фрагмент?', '''int g(int x = 5, int y = 10);
int g(int x, int y) { return x + y; }
int main() {
    std::cout << g() << '\\n';
}''', wrap='inc', why='Значения по умолчанию из объявления: 5 + 10 = <b>15</b>. В определении их повторять не нужно (и нельзя).')
add(4, '4.4', '10', 'Что выведет фрагмент?', '''void print(int x) {
    if (x < 0) return;
    std::cout << x;
}
int main() {
    print(-3);
}''', wrap='inc', ans=[''], why='<code>return;</code> досрочно выходит из void-функции: <b>ничего</b> не печатается.')
add(4, '4.5', '10', 'Что выведет фрагмент?', '''int counter() {
    static int x = 1;
    return x++;
}
int main() {
    std::cout << counter() << counter();
}''', wrap='inc', why='Статическая переменная живёт между вызовами: 1, потом 2 → <b>12</b>. (С C++17 операнды <code>&lt;&lt;</code> вычисляются слева направо.)')
add(4, '4.6', '10', 'Что выведет фрагмент?', '''int acc(int v) {
    static int t = 0;
    t += v;
    return t;
}
int main() {
    std::cout << acc(2) << acc(3);
}''', wrap='inc', why='2, затем 2 + 3 = 5 → <b>25</b>.')
add(4, '4.7', '10', 'Что выведет фрагмент?', '''void side() {
    static int calls = 0;
    std::cout << ++calls;
}
int main() {
    side(); side(); side();
}''', wrap='inc', why='<b>123</b>: счётчик сохраняется между вызовами.')
add(4, '4.8', '10', 'Что выведет фрагмент?', '''int minus(int x) { return -x; }
int minus(int x, int y) { return x - y; }
int main() {
    std::cout << minus(10) << minus(10, 3);
}''', wrap='inc', why='Перегрузка по числу параметров: −10 и 7 → <b>-107</b>.')
add(4, '4.9', '10', 'Что выведет код?', '''int reverse(int n, int rev = 0) {
    if (n == 0) return rev;
    return reverse(n / 10, rev * 10 + n % 10);
}
int main() {
    std::cout << reverse(123);
    return 0;
}''', wrap='inc', why='Хвостовая рекурсия с накопителем: (123, 0) → (12, 3) → (1, 32) → (0, 321) → <b>321</b>.')
add(4, '4.10', '10', 'Что выведет код?', '''int digitSum(int n) {
    if (n == 0) return 0;
    return (n % 10) + digitSum(n / 10);
}
int main() {
    std::cout << digitSum(123);
    return 0;
}''', wrap='inc', why='3 + 2 + 1 = <b>6</b>.')
add(4, '4.11', '10', 'Какие утверждения о функциях в C++ верны?', type='multi',
    opts=['Функция должна быть объявлена или определена до первого вызова', 'Объявление функции (declaration) не содержит тела', 'Определение функции (definition) содержит тело', 'Все функции обязаны иметь return', 'Функция без возвращаемого значения имеет тип void'], ans=[0, 1, 2, 4],
    why='<code>return</code> необязателен в <code>void</code>-функциях и в <code>main</code>. В остальных его отсутствие при использовании результата — UB, но не ошибка компиляции.')
add(4, '4.12', '10', 'Какие утверждения об аргументах по умолчанию верны?', type='multi',
    opts=['Аргументы по умолчанию указываются только в объявлении', 'Аргументы по умолчанию идут справа налево, без пропусков', 'Можно задать значение по умолчанию любому параметру независимо от позиции', 'Нельзя указывать значения по умолчанию и в объявлении, и в определении одновременно', 'Значения по умолчанию вычисляются при каждом вызове функции'], ans=[1, 3, 4],
    why='По умолчанию — только последние параметры (B). Указываются один раз, обычно в первом объявлении, повторять в определении нельзя (D). Выражение по умолчанию вычисляется заново при каждом вызове (E). Вариант A неточен: если отдельного объявления нет, значения пишут в определении.')
add(4, '4.13', '10', 'Что происходит при передаче аргументов по значению?', type='multi',
    opts=['Создаётся копия аргумента внутри функции', 'Изменения параметра внутри функции не влияют на исходную переменную', 'Передаётся адрес переменной'], ans=[0, 1],
    why='Адрес передаётся по указателю (а для ссылок — фактически тоже), но не при передаче по значению.')

# ---------------- Семинар 5 ----------------
add(5, '5.1', '13', 'Как объявить указатель на <code>int</code>?', type='single', opts=['<code>int ptr;</code>', '<code>pointer int ptr;</code>', '<code>*int ptr;</code>', '<code>int &amp;ptr;</code>', '<code>int* ptr;</code>'], ans=4,
    why='Звёздочка после типа: <code>int* ptr;</code>. <code>int&amp;</code> — ссылка, а не указатель.')
add(5, '5.2', '13', 'Как получить адрес переменной?', type='single', opts=['Операция <code>*</code>', 'Операция <code>&amp;</code>', 'Операция <code>-&gt;</code>', 'Операция <code>@</code>'], ans=1,
    why='<code>&amp;x</code> — адрес <code>x</code>. <code>*p</code> — наоборот, разыменование.')
add(5, '5.3', '13', 'Что такое разыменование указателя?', type='single', opts=['Получение адреса переменной', 'Получение значения (объекта) по адресу, хранящемуся в указателе', 'Изменение адреса указателя', 'Создание копии указателя'], ans=1,
    why='<code>*p</code> возвращает lvalue объекта, на который указывает <code>p</code>.')
add(5, '5.4', '13', 'Может ли указатель менять адрес, который он хранит?', type='single', opts=['Нет, только значение', 'Да, может указывать на другую переменную', 'Только если это константный указатель', 'Только через специальные функции'], ans=1,
    why='Обычный указатель — переменная, её можно переприсвоить. Нельзя только у константного указателя <code>int* const</code>.')
add(5, '5.5', '13', 'Что выведет фрагмент?', '''int a = 8, b = 4;
int *p = &a;
int *q = &b;
*p = *q * 2;
*q = *p - *q;
std::cout << a << ' ' << b;''', wrap='main', why='<code>a = 4 · 2 = 8</code>, затем <code>b = 8 − 4 = 4</code> → <b>8 4</b>.')
add(5, '5.6', '13', 'В чём разница между <code>const int*</code> и <code>int* const</code>?', type='single',
    opts=['Разницы нет', '<code>const int*</code> — указатель на константу, <code>int* const</code> — константный указатель', '<code>const int*</code> — константный указатель, <code>int* const</code> — указатель на константу', 'Оба выражения неверны'], ans=1,
    why='Читай справа налево: <code>int* const p</code> — «p — константный указатель на int».')
add(5, '5.7', '13', 'Что выведет фрагмент?', '''int a = 5, b = 10;
int *p1 = &a, *p2 = &b;
*p1 = *p2 + *p1;
std::cout << a << ' ' << b;''', wrap='main', why='a = 10 + 5 = 15, b не менялась.')
add(5, '5.8', '13', 'Что выведет фрагмент?', '''int x = 100;
int *ptr = &x;
int **pptr = &ptr;
**pptr = **pptr / *ptr;
std::cout << x;''', wrap='main', why='<code>**pptr</code> и <code>*ptr</code> — это всё <code>x</code>: 100 / 100 = <b>1</b>.')
add(5, '5.9', '13', 'Что выведет фрагмент?', '''int x = 10;
int *p = &x;
int **pp = &p;
int ***ppp = &pp;
***ppp = ***ppp + **pp + *p;
std::cout << x;''', wrap='main', why='Все три выражения — <code>x</code>: 10 + 10 + 10 = <b>30</b>.')
add(5, '5.10', '13', 'Что выведет фрагмент?', '''int x = 20, y = 30;
int *p = &x;
int *q = &y;
p = q;
*p = 40;
std::cout << x << ' ' << y;''', wrap='main', why='<code>p = q</code> перенаправляет указатель на <code>y</code>; запись идёт в <code>y</code> → <b>20 40</b>.')
add(5, '5.11', '13', 'Что выведет фрагмент?', '''int value = 7;
int *ptr1 = &value;
int *ptr2 = ptr1;
(*ptr1)++;
(*ptr2) *= 2;
std::cout << value;''', wrap='main', why='Оба указателя на <code>value</code>: (7 + 1) · 2 = <b>16</b>. Скобки в <code>(*ptr1)++</code> важны: без них инкрементировался бы указатель.')
add(5, '5.12', '13', 'Что выведет фрагмент?', '''int* generate() {
    int tmp = 999;
    return &tmp;
}

int main() {
    int *x = generate();
    std::cout << *x;
}''', wrap='inc', ans=['UB'], ub=True,
    why='Возвращается адрес локальной переменной, которая умерла при выходе из функции. <code>x</code> — висячий указатель, разыменование — <b>UB</b>. Может «случайно» напечатать 999, может мусор, может упасть.')
add(5, '5.13', '13', 'Что выведет фрагмент?', '''void swapPtr(int **p) {
    int local = 777;
    *p = &local;
}

int main() {
    int val = 111;
    int *ptr = &val;
    swapPtr(&ptr);
    std::cout << *ptr;
}''', wrap='inc', ans=['UB'], ub=True,
    why='Через указатель на указатель функция заставила <code>ptr</code> смотреть на свою локальную <code>local</code>, которая умерла. Дальше — висячий указатель и <b>UB</b>. (В оригинале на семинаре <code>cout</code> без <code>std::</code> — это ещё и CE без <code>using namespace std;</code>.)')
add(5, '5.14', '13', 'Что выведет фрагмент?', '''void triple(int *p) {
    *p = *p * 3;
}

int main() {
    int n = 15;
    triple(&n);
    std::cout << n;
}''', wrap='inc', why='Через указатель функция меняет оригинал: <b>45</b>.')

# ---------------- Семинар 7 ----------------
add(7, '7.1', '16', 'Что выведет фрагмент?', '''float arr[] = {1.5, 2.5, 3.5, 4.5};
float *ptr = arr + 3;
std::cout << ptr[-2] << " ";
std::cout << *(ptr - 1) << " ";
std::cout << (ptr - arr);''', wrap='main', why='<code>ptr</code> на arr[3]. <code>ptr[-2]</code> = arr[1] = 2.5, <code>*(ptr-1)</code> = arr[2] = 3.5, разность указателей — 3 элемента.')
add(7, '7.2', '16', 'Что выведет фрагмент?', '''int size = 3;
int *arr = new int[size]{30, 40, 50};
int *r = arr;
std::cout << *r << " ";
std::cout << *(r + 1) << " ";
std::cout << *r + 2;''', wrap='main', why='Ловушка приоритетов: <code>*r + 2</code> — это (30) + 2 = 32, а не arr[2]. (И не забыть бы <code>delete[] arr</code>.)')
add(7, '7.3', '16', 'Что выведет фрагмент?', '''int x = 1, y = 2, z = 3;
int *p[] = {&x, &y, &z};
int **q = p + 1;
std::cout << **q << " " << *(*(q + 1)) << " " << *p[2];''', wrap='main', why='<code>p</code> — массив указателей. <code>q</code> указывает на p[1] (→ y = 2), <code>q + 1</code> — на p[2] (→ z = 3), <code>*p[2]</code> = 3.')
add(7, '7.4', '16', 'Что выведет фрагмент?', '''int* createArray() {
    int arr[3] = {1, 2, 3};
    return arr;
}

int main() {
    int *result = createArray();
    std::cout << result[0];
}''', wrap='inc', ans=['UB'], ub=True, why='Локальный массив умирает при выходе из функции. Возвращённый указатель висячий → <b>UB</b>.')
add(7, '7.5', '16', 'Что выведет фрагмент?', '''int *ptr = new int(5);
int *arr = new int[5];
for (int i = 0; i < 5; i++) {
    arr[i] = *ptr + i;
}
delete ptr;
std::cout << arr[3];
delete[] arr;''', wrap='main', why='arr = {5, 6, 7, 8, 9} заполнен до <code>delete ptr</code>, так что arr[3] = <b>8</b>. Всё корректно: <code>delete</code> для одиночного, <code>delete[]</code> для массива.')
add(7, '7.6', '16', 'Что выведет фрагмент?', '''int a[] = {5, 10, 15};
int *p = a;
std::cout << *p++ << " ";
std::cout << *++p << " ";
std::cout << ++*p;''', wrap='main', why='<code>*p++</code>: прочитать a[0] = 5, затем сдвинуть p. <code>*++p</code>: сдвинуть на a[2], прочитать 15. <code>++*p</code>: увеличить a[2] до 16.')
add(7, '7.7', '16', 'Что будет выведено?', '''#include <iostream>

void modify(int arr[]) {
    arr[0] = 100;
    arr[1] = 200;
}

int main() {
    int nums[] = {1, 2, 3};
    modify(nums);
    std::cout << nums[0] << " " << nums[1];
    return 0;
}''', why='Массив передаётся как указатель на первый элемент, функция меняет оригинал → <b>100 200</b>.')
add(7, '7.8', '16', 'Что будет выведено?', '''#include <iostream>

int process(int* arr) {
    return *(arr + 2) + arr[1];
}

int main() {
    int data[] = {10, 20, 30, 40};
    int result = process(data);
    std::cout << result;
    return 0;
}''', why='30 + 20 = <b>50</b>.')
add(7, '7.9', '16', 'Что будет выведено?', '''#include <iostream>

int* getElement(int arr[], int index) {
    return &arr[index];
}

int main() {
    int values[] = {15, 25, 35, 45};
    int* ptr = getElement(values, 2);
    *ptr = 99;
    std::cout << values[2];
    return 0;
}''', why='Указатель на элемент массива из <code>main</code> — массив жив, всё законно: <b>99</b>.')
add(7, '7.10', '16', 'Что будет выведено?', '''#include <iostream>

int* findMid(int arr[], int size) {
    return arr + size/2;
}

int main() {
    int numbers[] = {5, 10, 15, 20, 25};
    int* mid = findMid(numbers, 5);
    *mid = 100;
    std::cout << numbers[2];
    return 0;
}''', why='5 / 2 = 2 → указатель на numbers[2], туда записали 100.')

# ---------------- Семинар 9 ----------------
add(9, '9.1', '19', 'Что будет в результате исполнения фрагмента?', '''int arr[2][3][2] = {
    {{10, 20}, {30, 40}, {50, 60}},
    {{70, 80}, {90, 100}, {110, 120}}
};
std::cout << *(**arr + 1) << " ";
std::cout << *(*(*(arr + 1) + 2)) << " ";
std::cout << arr[0][2][1];''', wrap='main', why='<code>**arr</code> — указатель на arr[0][0][0], +1 → 20. <code>*(*(arr + 1) + 2)</code> — arr[1][2], его первый элемент 110. <code>arr[0][2][1]</code> = 60.')
add(9, '9.2', '19', 'Что будет в результате исполнения фрагмента?', '''int a[3][2] = {9, 8, 7, 6, 5, 4};
int *p = &a[0][0];
std::cout << *(p + 4) << " ";
std::cout << a[2][0] << " ";
std::cout << (*(a + 1))[1];''', wrap='main', why='Плоская раскладка 9 8 | 7 6 | 5 4. Позиция 4 → 5; a[2][0] = 5; a[1][1] = 6.')
add(9, '9.3', '19', 'Что будет в результате исполнения фрагмента?', '''int matrix[2][3] = {{1, 2, 3}, {4, 5, 6}};
std::cout << *(matrix[1] + 1) << " ";
std::cout << *(*matrix + 4) << " ";
std::cout << (*(matrix + 1))[2];''', wrap='main', why='matrix[1][1] = 5; позиция 4 в плоской записи 1 2 3 4 5 6 → 5; matrix[1][2] = 6.')
add(9, '9.4', '19', 'Что будет в результате исполнения фрагмента?', '''int **arr = new int*[2];
for (int i = 0; i < 2; i++) {
    arr[i] = new int[3];
    for (int j = 0; j < 3; j++) {
        arr[i][j] = i * 3 + j + 1;
    }
}
std::cout << *(*(arr + 1) + 2);''', wrap='main', why='arr[1][2] = 1·3 + 2 + 1 = <b>6</b>. (Память здесь так и не освобождена — на семинаре за это снимают баллы.)')

# ---------------- Семинар 11 ----------------
add(11, '11.1', '20', 'Что выведет код?', '''struct Point {
    int x;
    int y;
};

int main() {
    Point p;
    std::cout << p.x << ' ' << p.y;
}''', wrap='inc', ans=['UB'], ub=True, why='Поля локальной структуры без инициализации — мусор, чтение — <b>UB</b>. <code>Point p{};</code> обнулил бы их.')
add(11, '11.2', '24', 'Что выведет код?', '''struct Point {
    Point() { std::cout << "Point() "; }
    ~Point() { std::cout << "~Point() "; }
};

int main() {
    Point p;
}''', wrap='inc', why='Конструктор при создании, деструктор в конце <code>main</code>.')
add(11, '11.3', '23', 'Что выведет код?', '''struct Point {
    int x;
    int y;

    Point(int x, int y) : x(x), y(y) {
        std::cout << "Point(" << x << "," << y << ") ";
    }
};

int main() {
    Point p1(1, 2);
    Point p2 = {3, 4};
    Point p3{5, 6};
}''', wrap='inc', why='Все три синтаксиса вызывают один и тот же конструктор. В списке инициализации <code>x(x)</code>: поле <code>x</code> инициализируется параметром <code>x</code> — так можно.')
add(11, '11.4', '25', 'Что выведет код?', '''struct Array {
    int* data;
    size_t size;

    Array(size_t n) : size(n) {
        data = new int[n];
        std::cout << "Array() ";
    }

    ~Array() {
        delete[] data;
        std::cout << "~Array() ";
    }
};

int main() {
    Array a(5);
    Array b = a; // проблема!
}''', wrap='inc', ans=['UB'], ub=True,
    why='Сгенерированный конструктор копирования скопировал указатель: <code>a.data == b.data</code>. Конструктор Array() отработает один раз, а оба деструктора сделают <code>delete[]</code> одной памяти — <b>double free, UB</b> (обычно падение после «Array() ~Array() »). Лечится правилом трёх.')
add(11, '11.5', '23', 'Что выведет код?', '''struct Point {
    int x;
    int y;

    Point() : x(0), y(0) { std::cout << "1 "; }
    Point(int x) : x(x), y(0) { std::cout << "2 "; }
    Point(int x, int y) : x(x), y(y) { std::cout << "3 "; }
};

int main() {
    Point p1;
    Point p2(5);
    Point p3(1, 2);
    Point p4{};
    Point p5 = 10;
}''', wrap='inc', why='p1 и p4 — конструктор по умолчанию (1), p2 и p5 — конструктор преобразования (2; он не <code>explicit</code>, поэтому <code>= 10</code> работает), p3 — (3).')

# ---------------- Ссылки и прочее (семинар 6 — вопросы из конспекта) ----------------
add(6, '6.к1', '14', 'Что выведет программа?', '''#include <iostream>
int main() {
    int x = 0;
    int y = 1;
    int& rx = x;
    rx = y;
    y = 5;
    std::cout << x << ' ' << rx << ' ' << y;
}''', why='<code>rx = y</code> — присваивание значения (x = 1), а не перепривязка. Дальнейшие изменения <code>y</code> на <code>x</code> не влияют → <b>1 1 5</b>.')
add(6, '6.к2', '15', 'Что выведет программа?', '''#include <iostream>
#include <memory>
int main() {
    auto p1 = std::make_shared<int>(100);
    {
        auto p2 = p1;
        *p2 += 1;
        std::cout << p1.use_count() << ' ';
    }
    std::cout << *p1 << ' ' << p1.use_count();
}''', why='Внутри блока два владельца, объект общий (101). После блока счётчик снова 1.')

def main():
    bad = 0; out = []
    ids = set()
    for i, q in enumerate(Q):
        qid = 's%s-%s' % (q['sem'], q['n'].replace('.', '-'))
        assert qid not in ids, qid; ids.add(qid)
        item = {'id': qid, 'sem': q['sem'], 'n': q['n'], 'ch': q['ch'], 'type': q['type'], 'q': q['q'], 'why': q.get('why', '')}
        for k in ('opts', 'ph', 'stdin'):
            if k in q: item[k] = q[k]
        if q.get('ub'): item['ub'] = True
        if q.get('code'):
            item['code'] = q['code']
            if q.get('wrap'): item['wrap'] = q['wrap']
        if q['type'] in ('single', 'multi', 'text', 'open'):
            if 'ans' in q: item['ans'] = q['ans']
        if q['type'] == 'out':
            rc, o = run(full_code(q), q.get('stdin', ''))
            if rc == 'CE':
                print('CE in', qid, o[:400]); bad += 1; continue
            got = norm(o)
            if 'ans' in q:
                item['ans'] = q['ans']
                if not q.get('ub') and not q.get('plat') and got not in [norm(a) for a in q['ans']]:
                    print('MISMATCH', qid, repr(q['ans']), 'got', repr(got)); bad += 1
            else:
                item['ans'] = [got]
            item['real'] = got
        out.append(item)
    json.dump(out, open(os.path.join(ROOT, 'data', 'predict.json'), 'w'), ensure_ascii=False, indent=0)
    print(len(out), 'questions; problems:', bad)
main()
