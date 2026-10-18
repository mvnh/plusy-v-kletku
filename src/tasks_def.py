# -*- coding: utf-8 -*-
# Definitions of tasks. Executed by gen_tasks.py (task(), IO, io_starter available).

# ======================= Глава 1–2 =======================
task('hello', '01', 'Самая важная программа', 'easy', 'lect',
 '<p>Выведи строку <code>Hello, world!</code> и перевод строки.</p>',
 r'''#include <iostream>
int main() {
    std::cout << "Hello, world!\n";
    return 0;
}''', [''], out='<code>Hello, world!</code>', show=1)

task('sum2', '02', 'Сумма двух чисел', 'easy', 'lect',
 '<p>Пример 1.22 из конспекта: даны два целых числа, выведи их сумму. Числа по модулю не больше 10⁹ — подумай, хватит ли <code>int</code> для суммы.</p>',
 r'''#include <iostream>
int main() {
    long long x, y;
    std::cin >> x >> y;
    std::cout << x + y << '\n';
}''', ['2 3', '-7 7', '1000000000 1000000000', '-1000000000 -999999999'], inp='Два целых числа через пробел.', out='Одно число — сумма.',
 hint='Два миллиарда в <code>int</code> не влезает (максимум ≈ 2,147·10⁹, а сумма может быть 2·10⁹ — влезает, но едва; и это граница). Надёжнее читать в <code>long long</code>.')

task('ranges', '02', 'Диапазоны без зубрёжки', 'easy', 'lect',
 '<p>Упражнения 2.1–2.3: выведи диапазоны типов <code>short</code>, <code>int</code>, <code>unsigned int</code>, <code>long long</code> — каждый в своей строке в формате <code>тип: min max</code>. Не вписывай числа руками: используй <code>&lt;climits&gt;</code> или <code>std::numeric_limits</code>.</p>',
 r'''#include <iostream>
#include <climits>
int main() {
    std::cout << "short: " << SHRT_MIN << ' ' << SHRT_MAX << '\n';
    std::cout << "int: " << INT_MIN << ' ' << INT_MAX << '\n';
    std::cout << "unsigned int: " << 0 << ' ' << UINT_MAX << '\n';
    std::cout << "long long: " << LLONG_MIN << ' ' << LLONG_MAX << '\n';
}''', [''], out='Четыре строки вида <code>short: -32768 32767</code>.', show=1, starter=io_starter('#include <climits>\n'))

task('divmod', '02', 'Частное, остаток и проверка', 'easy', 'sem',
 '<p>Упражнение 2.1 семинара. Даны целые <code>a</code> и <code>b</code> (<code>b ≠ 0</code>). Выведи в одной строке через пробел: <code>a / b</code>, <code>a % b</code> и <code>true</code> или <code>false</code> — выполняется ли <code>a == (a / b) * b + (a % b)</code>.</p>',
 r'''#include <iostream>
int main() {
    int a, b;
    std::cin >> a >> b;
    std::cout << a / b << ' ' << a % b << ' ' << std::boolalpha << (a == (a / b) * b + (a % b)) << '\n';
}''', ['17 5', '-17 5', '17 -5', '0 3', '-9 -4'], inp='Два целых числа <code>a b</code>, <code>b ≠ 0</code>.', out='<code>частное остаток true|false</code>',
 hint='Вывести <code>true</code>/<code>false</code> словами поможет <code>std::boolalpha</code>. Обрати внимание на знак остатка у отрицательных.')

task('tolower', '02', 'Заглавную в строчную', 'easy', 'sem',
 '<p>Упражнение 2.3. Считай один символ. Если это заглавная латинская буква — выведи её строчной, иначе выведи символ без изменений. Без <code>&lt;cctype&gt;</code>, только арифметика с <code>char</code>.</p>',
 r'''#include <iostream>
int main() {
    char c;
    std::cin >> c;
    if (c >= 'A' && c <= 'Z') c = c - 'A' + 'a';
    std::cout << c << '\n';
}''', ['Q', 'q', 'A', 'Z', '7', '@'], inp='Один непробельный символ.', out='Один символ.',
 hint="Буквы в ASCII идут подряд: <code>c - 'A'</code> — номер буквы в алфавите, остаётся прибавить <code>'a'</code>.")

task('asciidigits', '02', 'ASCII-коды цифр', 'easy', 'sem',
 "<p>Упражнение 2.4. Выведи ASCII-коды всех цифр от <code>'0'</code> до <code>'9'</code>, по одной строке в формате <code>0: 48</code>.</p>",
 r'''#include <iostream>
int main() {
    for (char c = '0'; c <= '9'; ++c)
        std::cout << c << ": " << int(c) << '\n';
}''', [''], show=1, out='10 строк от <code>0: 48</code> до <code>9: 57</code>.')

task('fixed3', '02', 'Три знака после запятой', 'easy', 'sem',
 '<p>Упражнение 1.4. Прочитай вещественное число и выведи его ровно с тремя знаками после запятой.</p>',
 r'''#include <iostream>
#include <iomanip>
int main() {
    double x;
    std::cin >> x;
    std::cout << std::fixed << std::setprecision(3) << x << '\n';
}''', ['10.2427', '2', '-0.0004', '3.14159'], inp='Вещественное число.', out='Число с тремя знаками после запятой.', starter=io_starter('#include <iomanip>\n'),
 hint='Манипуляторы <code>std::fixed</code> и <code>std::setprecision(3)</code> из <code>&lt;iomanip&gt;</code>.')

task('rev3', '02', 'Переверни трёхзначное', 'easy', 'lc',
 '<p>Дано трёхзначное натуральное число. Выведи число, записанное теми же цифрами в обратном порядке (ведущие нули отбрасываются: 120 → 21). Только арифметика, без строк.</p>',
 r'''#include <iostream>
int main() {
    int n;
    std::cin >> n;
    int a = n / 100, b = n / 10 % 10, c = n % 10;
    std::cout << c * 100 + b * 10 + a << '\n';
}''', ['123', '120', '100', '909', '555'], inp='Трёхзначное число.', out='Перевёрнутое число.', hint='Цифры: <code>n / 100</code>, <code>n / 10 % 10</code>, <code>n % 10</code>.')

# ======================= Глава 3, 7 =======================
task('safeadd', '07', 'Сложение без переполнения', 'easy', 'lect',
 '<p>Даны два числа типа <code>int</code>. Если их сумма помещается в <code>int</code>, выведи её. Иначе выведи <code>overflow</code>. Нельзя допускать переполнения в вычислениях: проверяй <b>до</b> сложения или считай в более широком типе.</p>',
 r'''#include <iostream>
#include <climits>
int main() {
    int a, b;
    std::cin >> a >> b;
    long long s = static_cast<long long>(a) + b;
    if (s > INT_MAX || s < INT_MIN) std::cout << "overflow\n";
    else std::cout << s << '\n';
}''', ['1 2', '2147483647 1', '-2147483648 -1', '2000000000 -2000000000', '1000000000 1147483647', '1000000000 1147483648'],
 inp='Два целых числа в диапазоне <code>int</code>.', out='Сумма или <code>overflow</code>.', starter=io_starter('#include <climits>\n'),
 hint='<code>static_cast&lt;long long&gt;(a) + b</code> не переполнится, а дальше сравни с <code>INT_MAX</code> и <code>INT_MIN</code>.')

# ======================= Глава 5 =======================
task('bits9', '05', 'Три битовые операции', 'easy', 'sem',
 '<p>Упражнение 2.2. Дано целое неотрицательное <code>x</code>. Используя только битовые операции, выведи в одной строке через пробел: <code>x</code> с установленным 2-м битом (с нуля); <code>x</code> со сброшенным 3-м битом; <code>even</code> или <code>odd</code>.</p>',
 r'''#include <iostream>
int main() {
    unsigned x;
    std::cin >> x;
    std::cout << (x | (1u << 2)) << ' ' << (x & ~(1u << 3)) << ' ' << ((x & 1) ? "odd" : "even") << '\n';
}''', ['9', '0', '12', '255', '6'], inp='Число <code>x</code>.', out='<code>x|bit2 x&amp;~bit3 even|odd</code>', hint='Маски: <code>1 &lt;&lt; 2</code> и <code>~(1 &lt;&lt; 3)</code>, чётность — <code>x &amp; 1</code>.')

task('revbits', '05', 'Зеркальные биты', 'medium', 'sem',
 '<p>Упражнение 2.5. Дано число от 0 до 15. Переверни его биты в двоичной записи <b>минимальной нужной длины</b> (6 = <code>110</code> → <code>011</code> = 3). Выведи три строки: двоичную запись числа, перевёрнутую двоичную запись (с ведущими нулями, той же длины) и перевёрнутое число в десятичной. Для 0 запись — <code>0</code>.</p>',
 r'''#include <iostream>
int main() {
    int n;
    std::cin >> n;
    int len = 1;
    while ((n >> len) > 0) ++len;
    int rev = 0;
    for (int i = 0; i < len; ++i)
        if (n >> i & 1) rev |= 1 << (len - 1 - i);
    for (int i = len - 1; i >= 0; --i) std::cout << (n >> i & 1);
    std::cout << '\n';
    for (int i = len - 1; i >= 0; --i) std::cout << (rev >> i & 1);
    std::cout << '\n' << rev << '\n';
}''', ['6', '1', '8', '0', '13', '15', '10'], inp='Число 0..15.', out='Три строки.',
 hint='Сначала найди длину: сдвигай вправо, пока не станет 0. Бит <code>i</code> исходного числа становится битом <code>len - 1 - i</code> результата.')

task('xorswap', '05', 'Обмен через XOR', 'easy', 'sem',
 '<p>Упражнение 2.6. Даны два целых числа <code>a</code> и <code>b</code>. Поменяй их значения местами, используя только битовые операции (без третьей переменной), и выведи <code>a b</code>.</p>',
 r'''#include <iostream>
int main() {
    int a, b;
    std::cin >> a >> b;
    a ^= b;
    b ^= a;
    a ^= b;
    std::cout << a << ' ' << b << '\n';
}''', ['7 12', '0 5', '-3 3', '42 42'], inp='<code>a b</code>', out='<code>a b</code> после обмена.', hint='Три XOR подряд: <code>a ^= b; b ^= a; a ^= b;</code>')

task('popcount', '05', 'Количество единичных битов', 'easy', 'lc',
 '<p>LeetCode 191 «Number of 1 Bits». Дано беззнаковое 32-битное число. Выведи, сколько в его двоичной записи единиц.</p>',
 r'''#include <iostream>
#include <cstdint>
int main() {
    uint32_t x;
    std::cin >> x;
    int c = 0;
    while (x) { x &= x - 1; ++c; }
    std::cout << c << '\n';
}''', ['11', '128', '0', '4294967293', '4294967295', '1023'], inp='Число от 0 до 2³² − 1.', out='Количество единиц.',
 hint='Трюк Кернигана: <code>x &amp;= x - 1</code> гасит младшую единицу. Сколько раз так можно сделать до нуля — столько и единиц.')

task('singlenum', '05', 'Число без пары', 'easy', 'lc',
 '<p>LeetCode 136 «Single Number». Дано <code>n</code> чисел: каждое встречается ровно дважды, кроме одного. Найди его за O(n) по времени и O(1) по памяти.</p>',
 r'''#include <iostream>
int main() {
    int n, acc = 0;
    std::cin >> n;
    for (int i = 0; i < n; ++i) { int x; std::cin >> x; acc ^= x; }
    std::cout << acc << '\n';
}''', ['5\n2 2 1 4 4', '1\n7', '7\n4 1 2 1 2 9 4', '3\n-5 3 3', '9\n10 20 30 40 50 40 30 20 10'], inp='<code>n</code>, затем <code>n</code> целых чисел.', out='Одиночное число.',
 hint='Вспомни свойства XOR из главы 5: <code>a ^ a == 0</code>, <code>a ^ 0 == a</code>.')

task('pow2', '05', 'Степень двойки?', 'easy', 'lc',
 '<p>LeetCode 231. Дано целое <code>n</code>. Выведи <code>YES</code>, если это степень двойки (1, 2, 4, 8, …), иначе <code>NO</code>. Без циклов — одной битовой проверкой.</p>',
 r'''#include <iostream>
int main() {
    long long n;
    std::cin >> n;
    std::cout << (n > 0 && (n & (n - 1)) == 0 ? "YES" : "NO") << '\n';
}''', ['1', '16', '18', '0', '-8', '1073741824', '1073741823'], inp='Целое число.', out='<code>YES</code> или <code>NO</code>.',
 hint='У степени двойки ровно одна единица. <code>n &amp; (n - 1)</code> гасит младшую единицу. Не забудь про <code>n &lt;= 0</code>.')

# ======================= Глава 6 =======================
task('harmonic', '06', 'Гармонический ряд до машинного нуля', 'medium', 'sem',
 '<p>Упражнение 3.7. Суммируй <code>1/1 + 1/2 + 1/3 + …</code> в переменной типа <code>float</code>, пока очередное слагаемое ещё меняет сумму. Выведи количество просуммированных членов, после которых сумма перестала меняться (номер первого «бесполезного» члена минус 1), и саму сумму с 6 знаками после запятой.</p><p>Для <code>double</code> так сделать не выйдет: понадобилось бы около 10¹⁵ итераций, это годы. Попробуй объяснить, почему.</p>',
 r'''#include <iostream>
#include <iomanip>
int main() {
    float s = 0;
    int n = 0;
    while (true) {
        float next = s + 1.0f / (n + 1);
        if (next == s) break;
        s = next;
        ++n;
    }
    std::cout << n << ' ' << std::fixed << std::setprecision(6) << s << '\n';
}''', [''], show=1, out='<code>количество сумма</code>', starter=io_starter('#include <iomanip>\n'),
 hint='Считай <code>next = s + 1.0f / (n + 1)</code> и сравнивай с <code>s</code>. Когда слагаемое меньше половины шага между соседними float рядом с суммой, сложение его «съедает».')

task('epseq', '06', 'Сравнение с допуском', 'easy', 'lect',
 '<p>Даны два вещественных числа <code>a</code>, <code>b</code> и допуск <code>eps</code>. Выведи <code>equal</code>, если <code>|a − b| &lt; eps</code>, иначе <code>not equal</code>.</p>',
 r'''#include <iostream>
#include <cmath>
int main() {
    double a, b, eps;
    std::cin >> a >> b >> eps;
    std::cout << (std::fabs(a - b) < eps ? "equal" : "not equal") << '\n';
}''', ['0.3 0.30000000000000004 1e-9', '1 1.1 0.01', '-2.5 -2.5 1e-12', '100 100.0001 0.001'], inp='<code>a b eps</code>', out='<code>equal</code> или <code>not equal</code>.', starter=io_starter('#include <cmath>\n'))

# ======================= Глава 8 =======================
task('max3', '08', 'Максимум из трёх', 'easy', 'lect',
 '<p>Пример 1.77: даны три целых числа, выведи наибольшее. Используй вложенные <code>if</code>/<code>else</code>, без функций вроде <code>std::max</code>.</p>',
 r'''#include <iostream>
int main() {
    int x, y, z;
    std::cin >> x >> y >> z;
    if (x >= y) {
        if (x >= z) std::cout << x << '\n';
        else std::cout << z << '\n';
    } else if (y >= z) std::cout << y << '\n';
    else std::cout << z << '\n';
}''', ['4 9 7', '1 2 3', '3 2 1', '-5 -5 -5', '5 5 2'], inp='Три целых числа.', out='Максимум.')

task('safediv', '08', 'Деление или Error', 'easy', 'lect',
 '<p>Пример 1.64, но правильно. Даны неотрицательные целые <code>x</code> и <code>y</code>. Выведи <code>x / y</code>, если <code>y ≠ 0</code>, иначе <code>Error</code>. Подсказка из конспекта: тернарный оператор тут не сработает напрямую — почему?</p>',
 r'''#include <iostream>
int main() {
    int x, y;
    std::cin >> x >> y;
    if (y != 0) std::cout << x / y << '\n';
    else std::cout << "Error\n";
}''', ['17 5', '17 0', '0 3', '0 0'], inp='<code>x y</code>', out='Частное или <code>Error</code>.', hint='<code>?:</code> требует общего типа у веток, а у <code>int</code> и строкового литерала его нет. Используй <code>if</code>/<code>else</code>.')

task('sign', '08', 'Знак числа', 'easy', 'sem',
 '<p>Вопрос 3.12. Выведи <code>positive</code>, <code>zero</code> или <code>negative</code>.</p>',
 r'''#include <iostream>
int main() {
    int x;
    std::cin >> x;
    if (x > 0) std::cout << "positive\n";
    else if (x == 0) std::cout << "zero\n";
    else std::cout << "negative\n";
}''', ['5', '0', '-3'], inp='Целое число.', out='Одно слово.')

task('calcswitch', '08', 'Калькулятор на switch', 'easy', 'lect',
 '<p>Дано выражение <code>a op b</code>, где <code>op</code> — один из символов <code>+ - * / %</code>. Вычисли его в целых числах через <code>switch</code>. При делении или остатке на ноль выведи <code>Error</code>, при неизвестной операции — <code>Unknown</code>.</p>',
 r'''#include <iostream>
int main() {
    long long a, b;
    char op;
    std::cin >> a >> op >> b;
    switch (op) {
        case '+': std::cout << a + b << '\n'; break;
        case '-': std::cout << a - b << '\n'; break;
        case '*': std::cout << a * b << '\n'; break;
        case '/':
        case '%':
            if (b == 0) { std::cout << "Error\n"; break; }
            std::cout << (op == '/' ? a / b : a % b) << '\n';
            break;
        default: std::cout << "Unknown\n";
    }
}''', ['7 + 5', '7 - 10', '6 * 7', '7 / 2', '7 % 3', '1 / 0', '5 % 0', '2 ^ 3', '-7 / 2'], inp='<code>a op b</code> (через пробелы).', out='Результат, <code>Error</code> или <code>Unknown</code>.',
 hint="<code>/</code> и <code>%</code> можно обработать вместе: две метки подряд — проваливание без <code>[[fallthrough]]</code>, потому что между ними нет кода.")

task('leap', '08', 'Високосный год', 'easy', 'sem',
 '<p>Год високосный, если он кратен 400, либо кратен 4, но не кратен 100 (условие из упражнения 11.1). Выведи <code>YES</code> или <code>NO</code>.</p>',
 r'''#include <iostream>
int main() {
    int y;
    std::cin >> y;
    bool leap = y % 400 == 0 || (y % 4 == 0 && y % 100 != 0);
    std::cout << (leap ? "YES" : "NO") << '\n';
}''', ['2024', '1900', '2000', '2023', '2100', '1600'], inp='Год.', out='<code>YES</code> или <code>NO</code>.')

task('triangle', '08', 'Какой треугольник', 'easy', 'lc',
 '<p>Даны три положительных целых длины сторон. Выведи <code>invalid</code>, если треугольник не существует (сумма любых двух сторон должна быть строго больше третьей), иначе <code>equilateral</code> (все равны), <code>isosceles</code> (ровно две равны) или <code>scalene</code>.</p>',
 r'''#include <iostream>
int main() {
    long long a, b, c;
    std::cin >> a >> b >> c;
    if (a + b <= c || a + c <= b || b + c <= a) std::cout << "invalid\n";
    else if (a == b && b == c) std::cout << "equilateral\n";
    else if (a == b || b == c || a == c) std::cout << "isosceles\n";
    else std::cout << "scalene\n";
}''', ['3 3 3', '3 4 5', '5 5 8', '1 2 3', '10 1 1', '2 3 2'], inp='Три числа.', out='Одно слово.')

# ======================= Глава 9 =======================
task('sumn', '09', 'Сумма n чисел', 'easy', 'lect',
 '<p>Пример 1.87. Вводится <code>n</code>, затем <code>n</code> целых чисел. Выведи их сумму.</p>',
 r'''#include <iostream>
int main() {
    int n;
    std::cin >> n;
    long long sum = 0;
    while (n > 0) {
        int x;
        std::cin >> x;
        sum += x;
        --n;
    }
    std::cout << sum << '\n';
}''', ['3\n5 2 8', '0', '1\n-7', '5\n1000000000 1000000000 1000000000 1000000000 1000000000'], inp='<code>n</code> и <code>n</code> чисел.', out='Сумма.',
 hint='Сумма пяти миллиардов в <code>int</code> не влезет — копи в <code>long long</code>.')

task('sum1n', '09', 'Сумма от 1 до n', 'easy', 'sem',
 '<p>Упражнение 3.1. Вычисли сумму первых <code>n</code> натуральных чисел циклом. (А потом проверь себя формулой Гаусса.)</p>',
 r'''#include <iostream>
int main() {
    long long n, s = 0;
    std::cin >> n;
    for (long long i = 1; i <= n; ++i) s += i;
    std::cout << s << '\n';
}''', ['1', '10', '100', '0', '100000'], inp='Целое <code>n ≥ 0</code>.', out='Сумма.')

task('oddsum', '09', 'Сумма нечётных', 'easy', 'sem',
 '<p>Упражнение 3.2. Вычисли сумму первых <code>n</code> членов ряда 1, 3, 5, 7, …</p>',
 r'''#include <iostream>
int main() {
    long long n, s = 0;
    std::cin >> n;
    for (long long i = 0; i < n; ++i) s += 2 * i + 1;
    std::cout << s << '\n';
}''', ['1', '2', '5', '0', '1000'], inp='<code>n</code>', out='Сумма.', hint='Посмотри на ответы: 1, 4, 9, 25… Совпадение?')

task('distinct', '09', 'Различные цифры', 'easy', 'sem',
 '<p>Упражнение 3.3. Выведи все числа из диапазона [2000, 3000], в записи которых все четыре цифры различны, по одному в строке.</p>',
 r'''#include <iostream>
int main() {
    for (int n = 2000; n <= 3000; ++n) {
        int a = n / 1000, b = n / 100 % 10, c = n / 10 % 10, d = n % 10;
        if (a != b && a != c && a != d && b != c && b != d && c != d) std::cout << n << '\n';
    }
}''', [''], show=0, out='Числа по возрастанию, каждое в своей строке (их 224).', hint='Разбери число на 4 цифры и сравни все 6 пар.')

task('hundreds', '09', 'Цифра сотен', 'easy', 'sem',
 '<p>Упражнение 3.4. Для натурального <code>N</code> выведи третью справа цифру (разряд сотен). Если цифр меньше трёх — выведи 0.</p>',
 r'''#include <iostream>
int main() {
    long long n;
    std::cin >> n;
    std::cout << n / 100 % 10 << '\n';
}''', ['12345', '7', '987', '100', '50'], inp='<code>N</code>', out='Цифра.')

task('avgzero', '09', 'Среднее до нуля', 'medium', 'sem',
 '<p>Упражнение 3.5. Вводятся положительные числа, ввод заканчивается нулём (ноль не учитывается). Выведи сумму и среднее арифметическое с двумя знаками после запятой через пробел. Если до нуля чисел не было — выведи <code>empty</code>.</p>',
 r'''#include <iostream>
#include <iomanip>
int main() {
    long long sum = 0;
    int cnt = 0, x;
    while (std::cin >> x && x != 0) { sum += x; ++cnt; }
    if (cnt == 0) std::cout << "empty\n";
    else std::cout << sum << ' ' << std::fixed << std::setprecision(2) << double(sum) / cnt << '\n';
}''', ['4 8 15 16 23 42 0', '0', '5 0', '1 2 0', '3 3 4 0'], inp='Числа до 0.', out='<code>сумма среднее</code> или <code>empty</code>.', starter=io_starter('#include <iomanip>\n'),
 hint='Среднее считай в <code>double</code>: <code>double(sum) / cnt</code>, иначе будет целочисленное деление.')

task('f15n30', '09', 'Кратные 15, но не 30', 'easy', 'sem',
 '<p>Упражнение 3.6. Выведи количество трёхзначных чисел, кратных 15, но не кратных 30, а в следующей строке — сами эти числа через пробел.</p>',
 r'''#include <iostream>
int main() {
    int cnt = 0;
    for (int n = 100; n <= 999; ++n) if (n % 15 == 0 && n % 30 != 0) ++cnt;
    std::cout << cnt << '\n';
    bool first = true;
    for (int n = 100; n <= 999; ++n)
        if (n % 15 == 0 && n % 30 != 0) { std::cout << (first ? "" : " ") << n; first = false; }
    std::cout << '\n';
}''', [''], show=0, check='tokens', out='Две строки.')

task('fizzbuzz', '09', 'FizzBuzz', 'easy', 'lc',
 '<p>LeetCode 412. Для чисел от 1 до <code>n</code> выведи по строке: <code>FizzBuzz</code>, если число кратно 15; <code>Fizz</code>, если кратно 3; <code>Buzz</code>, если кратно 5; иначе само число.</p>',
 r'''#include <iostream>
int main() {
    int n;
    std::cin >> n;
    for (int i = 1; i <= n; ++i) {
        if (i % 15 == 0) std::cout << "FizzBuzz\n";
        else if (i % 3 == 0) std::cout << "Fizz\n";
        else if (i % 5 == 0) std::cout << "Buzz\n";
        else std::cout << i << '\n';
    }
}''', ['5', '15', '1', '30'], inp='<code>n</code>', out='<code>n</code> строк.', hint='Порядок проверок важен: сначала 15, иначе до FizzBuzz не дойдёт.')

task('palnum', '09', 'Число-палиндром', 'easy', 'lc',
 '<p>LeetCode 9. Дано целое число. Выведи <code>YES</code>, если оно читается одинаково слева направо и справа налево, иначе <code>NO</code>. Отрицательные — не палиндромы. Без строк.</p>',
 r'''#include <iostream>
int main() {
    long long x;
    std::cin >> x;
    if (x < 0) { std::cout << "NO\n"; return 0; }
    long long r = 0, t = x;
    while (t > 0) { r = r * 10 + t % 10; t /= 10; }
    std::cout << (r == x ? "YES" : "NO") << '\n';
}''', ['121', '-121', '10', '0', '1234321', '123'], inp='Целое.', out='<code>YES</code>/<code>NO</code>.', hint='Собери перевёрнутое число в цикле: <code>r = r * 10 + t % 10</code>.')

task('gcd', '09', 'НОД алгоритмом Евклида', 'easy', 'lect',
 '<p>Даны два натуральных числа. Выведи их наибольший общий делитель, используя алгоритм Евклида в цикле <code>while</code>.</p>',
 r'''#include <iostream>
int main() {
    long long a, b;
    std::cin >> a >> b;
    while (b != 0) {
        long long t = a % b;
        a = b;
        b = t;
    }
    std::cout << a << '\n';
}''', ['12 18', '17 5', '100 10', '1 1', '1071 462'], inp='<code>a b</code>', out='НОД.', hint='Пока <code>b ≠ 0</code>: <code>(a, b) → (b, a % b)</code>.')

task('primes', '09', 'Простые числа до n', 'medium', 'lect',
 '<p>Выведи через пробел все простые числа, не превосходящие <code>n</code> (n ≤ 10⁵). Если таких нет — пустую строку.</p>',
 r'''#include <iostream>
int main() {
    int n;
    std::cin >> n;
    bool first = true;
    for (int x = 2; x <= n; ++x) {
        bool prime = true;
        for (int d = 2; d * d <= x; ++d)
            if (x % d == 0) { prime = false; break; }
        if (prime) { std::cout << (first ? "" : " ") << x; first = false; }
    }
    std::cout << '\n';
}''', ['10', '1', '2', '30', '100'], inp='<code>n</code>', out='Простые через пробел.', check='tokens', hint='Делители достаточно перебирать до √x: <code>d * d &lt;= x</code>. Выход из внутреннего цикла — <code>break</code>.')

task('stairs', '09', 'Лесенка из звёздочек', 'easy', 'lect',
 '<p>Выведи «лесенку» из <code>n</code> строк: в <code>i</code>-й строке ровно <code>i</code> звёздочек.</p>',
 r'''#include <iostream>
int main() {
    int n;
    std::cin >> n;
    for (int i = 1; i <= n; ++i) {
        for (int j = 0; j < i; ++j) std::cout << '*';
        std::cout << '\n';
    }
}''', ['3', '1', '5'], inp='<code>n</code>', out='<code>n</code> строк.')

# ======================= Глава 10: функции =======================
task('square', '10', 'square: обычная и шаблонная', 'easy', 'sem',
 '<p>Упражнение 4.1. Напиши <b>шаблонную</b> функцию <code>square(x)</code>, возвращающую квадрат аргумента того же типа. Проверяющий <code>main</code> вызовет её для <code>int</code> и для <code>double</code>.</p>',
 r'''template <class T>
T square(T x) {
    return x * x;
}''', ['5 1.5', '-3 0.1', '0 -2'], mode='func',
 starter='''#include <iostream>

template <class T>
T square(T x) {
    // TODO
}
''',
 harness=r'''#include <iostream>
int main() {
    int a; double b;
    std::cin >> a >> b;
    std::cout << square(a) << ' ' << square(b) << '\n';
}''', inp='Проверяющий main читает <code>int a</code> и <code>double b</code>.', out='<code>square(a) square(b)</code>')

task('iseven', '10', 'isEven', 'easy', 'sem',
 '<p>Упражнение 4.2. Напиши функцию <code>bool isEven(int n)</code>: <code>true</code>, если <code>n</code> чётное. Учти отрицательные числа.</p>',
 r'''bool isEven(int n) {
    return n % 2 == 0;
}''', ['4', '7', '0', '-3', '-8'], mode='func', starter='bool isEven(int n) {\n    // TODO\n}\n',
 harness=r'''#include <iostream>
int main() {
    int n;
    std::cin >> n;
    std::cout << std::boolalpha << isEven(n) << '\n';
}''', inp='<code>n</code>', out='<code>true</code>/<code>false</code>', hint='<code>-3 % 2 == -1</code>, а не 1. Сравнивай остаток с нулём.')

task('sumrange', '10', 'sumRange', 'easy', 'sem',
 '<p>Упражнение 4.3. Напиши <code>long long sumRange(int a, int b)</code> — сумма всех целых от <code>a</code> до <code>b</code> включительно; если <code>a &gt; b</code>, вернуть 0.</p>',
 r'''long long sumRange(int a, int b) {
    long long s = 0;
    for (long long i = a; i <= b; ++i) s += i;
    return s;
}''', ['1 10', '5 5', '10 1', '-3 3', '-5 -1'], mode='func', starter='long long sumRange(int a, int b) {\n    // TODO\n}\n',
 harness=r'''#include <iostream>
int main() {
    int a, b;
    std::cin >> a >> b;
    std::cout << sumRange(a, b) << '\n';
}''', inp='<code>a b</code>', out='Сумма.')

task('countdigits', '10', 'countDigits рекурсивно', 'easy', 'sem',
 '<p>Упражнение 4.4. Напиши <b>рекурсивную</b> функцию <code>int countDigits(int n)</code> — количество цифр числа (для отрицательных без учёта знака). У числа 0 одна цифра.</p>',
 r'''int countDigits(int n) {
    if (n < 0) n = -n;
    if (n < 10) return 1;
    return 1 + countDigits(n / 10);
}''', ['12345', '0', '-907', '7', '1000000000'], mode='func', starter='int countDigits(int n) {\n    // TODO: базовый случай + рекурсивный шаг\n}\n',
 harness=r'''#include <iostream>
int main() {
    int n;
    std::cin >> n;
    std::cout << countDigits(n) << '\n';
}''', inp='<code>n</code>', out='Количество цифр.', hint='Базовый случай: однозначное число (<code>n &lt; 10</code>) — 1 цифра. Шаг: <code>1 + countDigits(n / 10)</code>.')

task('power', '10', 'power рекурсивно', 'easy', 'sem',
 '<p>Упражнение 4.5. Напиши рекурсивную <code>long long power(long long base, int exp)</code>, <code>exp ≥ 0</code>.</p>',
 r'''long long power(long long base, int exp) {
    if (exp == 0) return 1;
    return base * power(base, exp - 1);
}''', ['2 10', '5 0', '-3 3', '10 18', '7 1'], mode='func', starter='long long power(long long base, int exp) {\n    // TODO\n}\n',
 harness=r'''#include <iostream>
int main() {
    long long b; int e;
    std::cin >> b >> e;
    std::cout << power(b, e) << '\n';
}''', inp='<code>base exp</code>', out='<code>base^exp</code>')

task('sumdigits', '10', 'sumDigits рекурсивно', 'easy', 'sem',
 '<p>Упражнение 4.6. Напиши рекурсивную <code>int sumDigits(int n)</code> — сумма цифр неотрицательного числа.</p>',
 r'''int sumDigits(int n) {
    if (n == 0) return 0;
    return n % 10 + sumDigits(n / 10);
}''', ['123', '0', '9999', '1000000000'], mode='func', starter='int sumDigits(int n) {\n    // TODO\n}\n',
 harness=r'''#include <iostream>
int main() {
    int n;
    std::cin >> n;
    std::cout << sumDigits(n) << '\n';
}''', inp='<code>n</code>', out='Сумма цифр.')

task('maxoverload', '10', 'Перегруженный max', 'easy', 'sem',
 '<p>Упражнение 4.7. Напиши две перегрузки: <code>int max(int a, int b)</code> и <code>double max(double a, double b)</code>.</p>',
 r'''int max(int a, int b) { return a > b ? a : b; }
double max(double a, double b) { return a > b ? a : b; }''', ['3 7 2.5 1.5', '-1 -9 -0.5 -0.25', '4 4 1 1'], mode='func',
 starter='int max(int a, int b) {\n    // TODO\n}\n\ndouble max(double a, double b) {\n    // TODO\n}\n',
 harness=r'''#include <iostream>
int main() {
    int a, b; double c, d;
    std::cin >> a >> b >> c >> d;
    std::cout << max(a, b) << ' ' << max(c, d) << '\n';
}''', inp='<code>int int double double</code>', out='Два максимума.')

task('printvalue', '10', 'printValue для трёх типов', 'easy', 'sem',
 '<p>Упражнение 4.8. Напиши три перегрузки <code>printValue</code>: для <code>int</code>, <code>double</code> и <code>bool</code>. Каждая печатает значение, пробел и тип в скобках, затем перевод строки: <code>5 (int)</code>, <code>2.5 (double)</code>, <code>true (bool)</code> (bool — словом).</p>',
 r'''#include <iostream>
void printValue(int x) { std::cout << x << " (int)\n"; }
void printValue(double x) { std::cout << x << " (double)\n"; }
void printValue(bool x) { std::cout << std::boolalpha << x << std::noboolalpha << " (bool)\n"; }''', ['5 2.5 1', '-3 0.125 0'], mode='func',
 starter='#include <iostream>\n\nvoid printValue(int x) {\n}\n\nvoid printValue(double x) {\n}\n\nvoid printValue(bool x) {\n}\n',
 harness=r'''int main() {
    int a; double b; int c;
    std::cin >> a >> b >> c;
    printValue(a);
    printValue(b);
    printValue(c != 0);
}''', inp='Main прочитает int, double и 0/1 для bool.', out='Три строки.')

task('fib', '10', 'Числа Фибоначчи', 'easy', 'lc',
 '<p>LeetCode 509. <code>F(0) = 0, F(1) = 1, F(n) = F(n−1) + F(n−2)</code>. Напиши <code>long long fib(int n)</code> для <code>0 ≤ n ≤ 90</code>. Рекурсия «в лоб» не уложится во время на n = 90 (вспомни Ω(1,5ⁿ) из конспекта) — нужна итерация.</p>',
 r'''long long fib(int n) {
    long long a = 0, b = 1;
    for (int i = 0; i < n; ++i) {
        long long t = a + b;
        a = b;
        b = t;
    }
    return a;
}''', ['0', '1', '10', '50', '90'], mode='func', starter='long long fib(int n) {\n    // TODO\n}\n',
 harness=r'''#include <iostream>
int main() {
    int n;
    std::cin >> n;
    std::cout << fib(n) << '\n';
}''', inp='<code>n</code>', out='<code>F(n)</code>', hint='Храни два последних значения и сдвигай их на каждом шаге.')

task('hanoi', '10', 'Ханойская башня', 'medium', 'lect',
 '<p>Классика рекурсии. Переложи <code>n</code> дисков со стержня 1 на стержень 3, используя 2 как вспомогательный. Большой диск нельзя класть на меньший. Напиши <code>void hanoi(int n, int from, int to, int via)</code>, которая печатает каждый ход строкой <code>from to</code>. Проверяющий main выведет ещё и число ходов.</p>',
 r'''#include <iostream>
int moves = 0;
void hanoi(int n, int from, int to, int via) {
    if (n == 0) return;
    hanoi(n - 1, from, via, to);
    std::cout << from << ' ' << to << '\n';
    ++moves;
    hanoi(n - 1, via, to, from);
}''', ['1', '2', '3', '5'], mode='func',
 starter='#include <iostream>\nint moves = 0; // увеличивай при каждом ходе\n\nvoid hanoi(int n, int from, int to, int via) {\n    // TODO: переложи n-1 на via, большой на to, n-1 с via на to\n}\n',
 harness=r'''int main() {
    int n;
    std::cin >> n;
    hanoi(n, 1, 3, 2);
    std::cout << "moves: " << moves << '\n';
}''', inp='<code>n ≤ 10</code>', out='Ходы и итог.', hint='Чтобы переложить n дисков: переложи n−1 на вспомогательный, самый большой — на цель, потом n−1 с вспомогательного на цель. Всего 2ⁿ − 1 ходов.')

# ======================= Глава 13: указатели =======================
task('swapint', '13', 'swap_int через указатели', 'easy', 'sem',
 '<p>Упражнение 5.1. Напиши <code>void swap_int(int* a, int* b)</code>, меняющую местами значения по указателям.</p>',
 r'''void swap_int(int* a, int* b) {
    int t = *a;
    *a = *b;
    *b = t;
}''', ['3 8', '-1 1', '5 5'], mode='func', starter='void swap_int(int* a, int* b) {\n    // TODO\n}\n',
 harness=r'''#include <iostream>
int main() {
    int x, y;
    std::cin >> x >> y;
    swap_int(&x, &y);
    std::cout << x << ' ' << y << '\n';
}''', inp='Два числа.', out='Числа после обмена.')

task('inc10', '13', '+10% по указателю', 'easy', 'sem',
 '<p>Упражнение 5.2. Напиши <b>шаблонную</b> функцию <code>increase_by_10_percent(T* price)</code>, увеличивающую значение по указателю на 10%.</p>',
 r'''template <class T>
void increase_by_10_percent(T* price) {
    *price = *price * 1.1;
}''', ['100', '19.99', '0'], mode='func', starter='template <class T>\nvoid increase_by_10_percent(T* price) {\n    // TODO\n}\n',
 harness=r'''#include <iostream>
#include <iomanip>
int main() {
    double p; std::cin >> p;
    float f = static_cast<float>(p);
    increase_by_10_percent(&p);
    increase_by_10_percent(&f);
    std::cout << std::fixed << std::setprecision(2) << p << ' ' << f << '\n';
}''', inp='Цена.', out='Цена после повышения (для double и float).', check='float')

task('minptr', '13', 'Указатель на минимум', 'easy', 'sem',
 '<p>Упражнение 5.3. Напиши <code>int* min_ptr(int* a, int* b)</code>, возвращающую указатель на меньшее из двух значений (при равенстве — <code>a</code>). Проверяющий main проверит, что вернулся именно адрес одной из переменных, а не копии.</p>',
 r'''int* min_ptr(int* a, int* b) {
    return *b < *a ? b : a;
}''', ['3 8', '8 3', '-5 -5', '0 -1'], mode='func', starter='int* min_ptr(int* a, int* b) {\n    // TODO\n}\n',
 harness=r'''#include <iostream>
int main() {
    int x, y;
    std::cin >> x >> y;
    int* p = min_ptr(&x, &y);
    std::cout << (p == &x ? "x" : p == &y ? "y" : "?") << ' ' << *p << '\n';
    *p = 100;
    std::cout << x << ' ' << y << '\n';
}''', inp='Два числа.', out='Какая переменная и её значение; потом значения после записи 100 по указателю.')

task('staticctr', '13', 'Статический счётчик по указателю', 'easy', 'sem',
 '<p>Упражнение 5.5. Напиши <code>int* get_static_counter()</code>: статическая локальная <code>count</code> (начально 0) увеличивается при каждом вызове, функция возвращает указатель на неё. Почему это не висячий указатель?</p>',
 r'''int* get_static_counter() {
    static int count = 0;
    ++count;
    return &count;
}''', ['3', '1'], mode='func', starter='int* get_static_counter() {\n    // TODO\n}\n',
 harness=r'''#include <iostream>
int main() {
    int n; std::cin >> n;
    int* first = get_static_counter();
    bool same = true;
    for (int i = 1; i < n; ++i) same = same && (get_static_counter() == first);
    std::cout << *first << ' ' << (same ? "same address" : "different") << '\n';
}''', inp='Сколько раз вызвать.', out='Значение счётчика и проверка адреса.', solNote='Статическая переменная живёт до конца программы, поэтому указатель на неё никогда не повиснет. В реальных проектах так делать не советуют: это скрытое глобальное состояние, его может поменять любой, кто получил указатель.')

task('adjust', '13', 'Инфляция двух цен', 'easy', 'sem',
 '<p>Упражнение 5.6. Напиши <code>void adjust_prices(double* p1, double* p2, double inflation_rate)</code>, увеличивающую обе цены на долю <code>inflation_rate</code> (0.05 — это 5%).</p>',
 r'''void adjust_prices(double* p1, double* p2, double inflation_rate) {
    *p1 *= 1 + inflation_rate;
    *p2 *= 1 + inflation_rate;
}''', ['100 200 0.05', '10 0 0.5', '99.9 1 0'], mode='func', starter='void adjust_prices(double* p1, double* p2, double inflation_rate) {\n    // TODO\n}\n',
 harness=r'''#include <iostream>
#include <iomanip>
int main() {
    double a, b, r;
    std::cin >> a >> b >> r;
    adjust_prices(&a, &b, r);
    std::cout << std::fixed << std::setprecision(2) << a << ' ' << b << '\n';
}''', inp='<code>p1 p2 rate</code>', out='Новые цены.', check='float')

task('bytes', '13', 'Байты числа через char*', 'medium', 'sem',
 '<p>Упражнение 5.7. Дано 32-битное <code>int</code>. Используя только указатели (без массивов и битовых операций), выведи его 4 байта <b>в порядке их расположения в памяти</b> — как числа от 0 до 255 через пробел. Подсказка: <code>unsigned char*</code>. На little-endian машинах (x86, ARM, WebAssembly) младший байт лежит первым.</p>',
 r'''#include <iostream>
int main() {
    int x;
    std::cin >> x;
    unsigned char* p = reinterpret_cast<unsigned char*>(&x);
    for (int i = 0; i < 4; ++i) std::cout << int(*(p + i)) << (i < 3 ? " " : "\n");
}''', ['1633837924', '1', '-1', '256', '0'], inp='Целое число (для 0x61626364 это 1633837924).', out='4 числа.',
 hint='<code>unsigned char* p = reinterpret_cast&lt;unsigned char*&gt;(&amp;x);</code> — дальше <code>*(p + i)</code>. Печатай через <code>int(...)</code>, иначе выйдут символы.')

task('sort3cmp', '13', 'Сортировка трёх с компаратором', 'medium', 'sem',
 '<p>Упражнение 5.8. Напиши <code>void sort_three(double* x, double* y, double* z, bool (*compare)(double, double))</code>, которая переставляет значения так, чтобы для соседей выполнялось <code>compare</code>-упорядочение, и две функции <code>ascending</code> и <code>descending</code>.</p>',
 r'''bool ascending(double a, double b) { return a < b; }
bool descending(double a, double b) { return a > b; }
void sort_three(double* x, double* y, double* z, bool (*compare)(double, double)) {
    auto sw = [](double* a, double* b) { double t = *a; *a = *b; *b = t; };
    if (compare(*y, *x)) sw(x, y);
    if (compare(*z, *y)) sw(y, z);
    if (compare(*y, *x)) sw(x, y);
}''', ['5.2 3.8 7.1', '1 2 3', '3 2 1', '2 2 1'], mode='func',
 starter='bool ascending(double a, double b) { return a < b; }\nbool descending(double a, double b) { return a > b; }\n\nvoid sort_three(double* x, double* y, double* z, bool (*compare)(double, double)) {\n    // TODO\n}\n',
 harness=r'''#include <iostream>
int main() {
    double a, b, c;
    std::cin >> a >> b >> c;
    sort_three(&a, &b, &c, ascending);
    std::cout << a << ' ' << b << ' ' << c << '\n';
    sort_three(&a, &b, &c, descending);
    std::cout << a << ' ' << b << ' ' << c << '\n';
}''', inp='Три числа.', out='По возрастанию, потом по убыванию.', hint='Три сравнения-обмена: (x, y), (y, z), (x, y) — сеть сортировки на три элемента.')

task('printif', '13', 'Вывод по предикату', 'easy', 'sem',
 '<p>Упражнение 5.9. Напиши <code>void printIf(double v1, double v2, double v3, bool (*predicate)(double))</code>, печатающую через пробел (и в конце перевод строки) только те значения, для которых предикат истинен, и предикаты <code>isAbove100</code> и <code>isInflationary</code> (строго между 100 и 110).</p>',
 r'''#include <iostream>
bool isAbove100(double x) { return x > 100; }
bool isInflationary(double x) { return x > 100 && x < 110; }
void printIf(double v1, double v2, double v3, bool (*predicate)(double)) {
    bool first = true;
    for (double v : {v1, v2, v3})
        if (predicate(v)) { std::cout << (first ? "" : " ") << v; first = false; }
    std::cout << '\n';
}''', ['95 105 120', '101 102 103', '1 2 3'], mode='func',
 starter='#include <iostream>\n\nbool isAbove100(double x) {\n}\n\nbool isInflationary(double x) {\n}\n\nvoid printIf(double v1, double v2, double v3, bool (*predicate)(double)) {\n}\n',
 harness=r'''int main() {
    double a, b, c;
    std::cin >> a >> b >> c;
    printIf(a, b, c, isAbove100);
    printIf(a, b, c, isInflationary);
}''', inp='Три числа.', out='Две строки.', check='tokens')

# ======================= Глава 14: ссылки =======================
task('swaps', '14', 'Обмен: указатели vs ссылки', 'easy', 'sem',
 '<p>Упражнение 6.1. Напиши <code>void swapPtr(double* a, double* b)</code> и <code>void swapRef(double&amp; a, double&amp; b)</code>.</p>',
 r'''void swapPtr(double* a, double* b) { double t = *a; *a = *b; *b = t; }
void swapRef(double& a, double& b) { double t = a; a = b; b = t; }''', ['12.5 9.8', '1 2'], mode='func',
 starter='void swapPtr(double* a, double* b) {\n}\n\nvoid swapRef(double& a, double& b) {\n}\n',
 harness=r'''#include <iostream>
int main() {
    double a, b;
    std::cin >> a >> b;
    swapPtr(&a, &b);
    std::cout << a << ' ' << b << '\n';
    swapRef(a, b);
    std::cout << a << ' ' << b << '\n';
}''', inp='Две цены.', out='После swapPtr и после swapRef (вернутся исходные).')

task('funcref', '14', 'Ссылки на функции', 'medium', 'sem',
 '<p>Упражнение 6.2. Даны <code>add</code> и <code>multiply</code>. Допиши <code>int calculate(int x, int y, int (&amp;operation)(int, int))</code> и <code>int (&amp;get_operation(char op))(int, int)</code>, возвращающую ссылку на <code>add</code> для <code>\'+\'</code>, на <code>multiply</code> для <code>\'*\'</code>, иначе на <code>add</code>.</p>',
 r'''int add(int a, int b) { return a + b; }
int multiply(int a, int b) { return a * b; }
int calculate(int x, int y, int (&operation)(int, int)) {
    return operation(x, y);
}
int (&get_operation(char op))(int, int) {
    if (op == '*') return multiply;
    return add;
}''', ['5 3 +', '5 3 *', '10 20 -'], mode='func',
 starter='int add(int a, int b) { return a + b; }\nint multiply(int a, int b) { return a * b; }\n\nint calculate(int x, int y, int (&operation)(int, int)) {\n    // TODO\n}\n\nint (&get_operation(char op))(int, int) {\n    // TODO\n}\n',
 harness=r'''#include <iostream>
int main() {
    int x, y; char op;
    std::cin >> x >> y >> op;
    std::cout << calculate(x, y, add) << ' ' << calculate(x, y, multiply) << '\n';
    int (&f)(int, int) = get_operation(op);
    std::cout << f(x, y) << '\n';
}''', inp='<code>x y op</code>', out='Две строки.', hint='Синтаксис возврата ссылки на функцию страшный, но тело простое: <code>return multiply;</code>.')

task('sumprod', '14', 'Сумма и произведение через ссылки', 'easy', 'sem',
 '<p>Упражнение 6.3. Напиши <code>void calculate(int a, int b, int&amp; sum, int&amp; p)</code>, которая «возвращает» сразу два результата через ссылки.</p>',
 r'''void calculate(int a, int b, int& sum, int& p) {
    sum = a + b;
    p = a * b;
}''', ['7 3', '-2 5', '0 0'], mode='func', starter='void calculate(int a, int b, int& sum, int& p) {\n    // TODO\n}\n',
 harness=r'''#include <iostream>
int main() {
    int x, y, s, p;
    std::cin >> x >> y;
    calculate(x, y, s, p);
    std::cout << x << " + " << y << " = " << s << '\n' << x << " * " << y << " = " << p << '\n';
}''', inp='Два числа.', out='Две строки.')

task('sort3ref', '14', 'sortThree по ссылкам', 'easy', 'sem',
 '<p>Упражнение 6.5. Напиши <code>void swap(int&amp; x, int&amp; y)</code> и <code>void sortThree(int&amp; a, int&amp; b, int&amp; c)</code>, после которой <code>a ≤ b ≤ c</code>.</p>',
 r'''void swap(int& x, int& y) { int t = x; x = y; y = t; }
void sortThree(int& a, int& b, int& c) {
    if (b < a) swap(a, b);
    if (c < b) swap(b, c);
    if (b < a) swap(a, b);
}''', ['7 2 5', '1 2 3', '3 2 1', '5 5 1', '-1 0 -1'], mode='func', starter='void swap(int& x, int& y) {\n}\n\nvoid sortThree(int& a, int& b, int& c) {\n}\n',
 harness=r'''#include <iostream>
int main() {
    int x, y, z;
    std::cin >> x >> y >> z;
    sortThree(x, y, z);
    std::cout << x << ' ' << y << ' ' << z << '\n';
}''', inp='Три числа.', out='По возрастанию.')

# ======================= Глава 15 =======================
task('uniqsq', '15', 'Квадраты в unique_ptr', 'medium', 'lect',
 '<p>Напиши <code>std::unique_ptr&lt;int[]&gt; makeSquares(int n)</code>, возвращающую динамический массив <code>0², 1², …, (n−1)²</code>. Ни одного <code>delete</code> в программе быть не должно — память освободит <code>unique_ptr</code>.</p>',
 r'''#include <memory>
std::unique_ptr<int[]> makeSquares(int n) {
    auto a = std::make_unique<int[]>(n);
    for (int i = 0; i < n; ++i) a[i] = i * i;
    return a;
}''', ['5', '1', '10'], mode='func', starter='#include <memory>\n\nstd::unique_ptr<int[]> makeSquares(int n) {\n    // TODO: std::make_unique<int[]>(n)\n}\n',
 harness=r'''#include <iostream>
int main() {
    int n; std::cin >> n;
    std::unique_ptr<int[]> sq = makeSquares(n);
    for (int i = 0; i < n; ++i) std::cout << sq[i] << (i + 1 < n ? " " : "\n");
}''', inp='<code>n ≥ 1</code>', out='Квадраты через пробел.', hint='<code>std::make_unique&lt;int[]&gt;(n)</code> создаёт массив, а возврат <code>unique_ptr</code> из функции — это перемещение, копирования нет.')

# ======================= Глава 16: массивы =======================
task('arrmax', '16', 'Максимум массива', 'easy', 'lect',
 '<p>Пример 1.195. Дано <code>n</code> (1 ≤ n ≤ 100) и <code>n</code> чисел. Сохрани их в статический массив и выведи максимальное.</p>',
 r'''#include <iostream>
int main() {
    int n;
    std::cin >> n;
    int a[100];
    for (int i = 0; i < n; ++i) std::cin >> a[i];
    int mx = a[0];
    for (int i = 1; i < n; ++i) if (a[i] > mx) mx = a[i];
    std::cout << mx << '\n';
}''', ['5\n3 9 -2 9 4', '1\n-7', '4\n-5 -3 -9 -4'], inp='<code>n</code> и массив.', out='Максимум.', hint='Начни с <code>max = a[0]</code>, а не с нуля: все числа могут быть отрицательными.')

task('createinit', '16', 'createAndInit', 'easy', 'sem',
 '<p>Упражнение 7.1. Напиши <code>int* createAndInit(int size, int value)</code>: создаёт динамический массив и заполняет его значением <code>value</code>. Проверяющий main сам освободит память через <code>delete[]</code>.</p>',
 r'''int* createAndInit(int size, int value) {
    int* a = new int[size];
    for (int i = 0; i < size; ++i) a[i] = value;
    return a;
}''', ['4 7', '1 -1', '6 0'], mode='func', starter='int* createAndInit(int size, int value) {\n    // TODO\n}\n',
 harness=r'''#include <iostream>
int main() {
    int n, v; std::cin >> n >> v;
    int* a = createAndInit(n, v);
    for (int i = 0; i < n; ++i) std::cout << a[i] << (i + 1 < n ? " " : "\n");
    delete[] a;
}''', inp='<code>size value</code>', out='Массив.')

task('copyarr', '16', 'copyArray', 'easy', 'sem',
 '<p>Упражнение 7.2. Напиши <code>int* copyArray(const int* arr, int size)</code> — новый динамический массив-копию. Изменения копии не должны влиять на оригинал. Зачем <code>const</code> в параметре?</p>',
 r'''int* copyArray(const int* arr, int size) {
    int* c = new int[size];
    for (int i = 0; i < size; ++i) c[i] = arr[i];
    return c;
}''', ['3\n1 2 3', '1\n42', '5\n5 4 3 2 1'], mode='func', starter='int* copyArray(const int* arr, int size) {\n    // TODO\n}\n',
 harness=r'''#include <iostream>
int main() {
    int n; std::cin >> n;
    int* a = new int[n];
    for (int i = 0; i < n; ++i) std::cin >> a[i];
    int* c = copyArray(a, n);
    c[0] = -100;
    std::cout << (c != a ? "new memory" : "same memory!") << '\n';
    for (int i = 0; i < n; ++i) std::cout << a[i] << ' ';
    std::cout << '\n';
    for (int i = 0; i < n; ++i) std::cout << c[i] << ' ';
    std::cout << '\n';
    delete[] a; delete[] c;
}''', inp='Массив.', out='Проверка, оригинал, изменённая копия.', check='tokens')

task('resize', '16', 'resizeArray', 'medium', 'sem',
 '<p>Упражнение 7.3. Напиши <code>int* resizeArray(int* arr, int oldSize, int newSize)</code>: выделяет новый массив, копирует <code>min(oldSize, newSize)</code> элементов, остаток заполняет нулями, <b>освобождает старый</b> и возвращает новый.</p>',
 r'''int* resizeArray(int* arr, int oldSize, int newSize) {
    int* r = new int[newSize];
    for (int i = 0; i < newSize; ++i) r[i] = i < oldSize ? arr[i] : 0;
    delete[] arr;
    return r;
}''', ['3 6\n1 2 3', '6 2\n1 2 3 4 5 6', '2 2\n9 8'], mode='func', starter='int* resizeArray(int* arr, int oldSize, int newSize) {\n    // TODO\n}\n',
 harness=r'''#include <iostream>
int main() {
    int o, n; std::cin >> o >> n;
    int* a = new int[o];
    for (int i = 0; i < o; ++i) std::cin >> a[i];
    a = resizeArray(a, o, n);
    for (int i = 0; i < n; ++i) std::cout << a[i] << (i + 1 < n ? " " : "\n");
    delete[] a;
}''', inp='<code>oldSize newSize</code> и массив.', out='Новый массив.', hint='Самое важное — не забыть <code>delete[] arr</code> внутри функции. Иначе утечка.')

task('readprint', '16', 'readArray и printArray', 'medium', 'sem',
 '<p>Упражнение 7.4. Напиши <code>int* readArray(int&amp; size)</code> (читает размер и элементы со stdin, размер возвращает через ссылку; если размер ≤ 0 — возвращает <code>nullptr</code> и size = 0) и <code>void printArray(const int* arr, int size)</code>, печатающую <code>[10, 20, 30]</code> (для пустого/нулевого — <code>[]</code>).</p>',
 r'''#include <iostream>
int* readArray(int& size) {
    std::cin >> size;
    if (size <= 0) { size = 0; return nullptr; }
    int* a = new int[size];
    for (int i = 0; i < size; ++i) std::cin >> a[i];
    return a;
}
void printArray(const int* arr, int size) {
    std::cout << '[';
    for (int i = 0; arr != nullptr && i < size; ++i) std::cout << (i ? ", " : "") << arr[i];
    std::cout << "]\n";
}''', ['3\n10 20 30', '0', '-2', '1\n5'], mode='func',
 starter='#include <iostream>\n\nint* readArray(int& size) {\n    // TODO\n}\n\nvoid printArray(const int* arr, int size) {\n    // TODO\n}\n',
 harness=r'''int main() {
    int n = 0;
    int* a = readArray(n);
    printArray(a, n);
    delete[] a; // delete[] nullptr — безопасно
}''', inp='Размер и элементы.', out='<code>[a, b, c]</code>')

task('safedel', '16', 'safeDelete', 'easy', 'sem',
 '<p>Упражнение 7.5. Напиши <code>void safeDelete(int*&amp; ptr)</code>: если <code>ptr</code> не <code>nullptr</code>, делает <code>delete[]</code>, и в любом случае обнуляет указатель. Почему параметр — ссылка на указатель?</p>',
 r'''void safeDelete(int*& ptr) {
    if (ptr != nullptr) delete[] ptr;
    ptr = nullptr;
}''', ['5', '0'], mode='func', starter='void safeDelete(int*& ptr) {\n    // TODO\n}\n',
 harness=r'''#include <iostream>
int main() {
    int n; std::cin >> n;
    int* p = n > 0 ? new int[n] : nullptr;
    safeDelete(p);
    std::cout << (p == nullptr ? "null" : "dangling") << '\n';
    safeDelete(p);
    std::cout << "ok\n";
}''', inp='Размер.', out='Две строки.', solNote='Указатель передаётся по ссылке, чтобы обнулить <b>сам указатель</b> вызывающего, а не его копию.')

task('clone', '16', 'Шаблонный cloneArray', 'medium', 'sem',
 '<p>Упражнение 7.6. Напиши <code>template&lt;typename T&gt; T* cloneArray(const T* arr, int size)</code>. Проверка будет на <code>int</code>, <code>double</code> и <code>std::string</code>.</p>',
 r'''template <typename T>
T* cloneArray(const T* arr, int size) {
    T* c = new T[size];
    for (int i = 0; i < size; ++i) c[i] = arr[i];
    return c;
}''', ['3'], mode='func', starter='template <typename T>\nT* cloneArray(const T* arr, int size) {\n    // TODO\n}\n',
 harness=r'''#include <iostream>
#include <string>
int main() {
    int n; std::cin >> n;
    int ai[3]{1, 2, 3}; double ad[3]{0.5, 1.5, 2.5}; std::string as[3]{"a", "bb", "ccc"};
    int* ci = cloneArray(ai, n); double* cd = cloneArray(ad, n); std::string* cs = cloneArray(as, n);
    cs[0] += "!";
    for (int i = 0; i < n; ++i) std::cout << ci[i] << ' ' << cd[i] << ' ' << cs[i] << ' ' << as[i] << '\n';
    delete[] ci; delete[] cd; delete[] cs;
}''', inp='—', out='Таблица.', show=1)

task('bubble', '16', 'Пузырёк с компаратором', 'medium', 'sem',
 '<p>Упражнение 7.7. Напиши <code>void bubbleSort(int* arr, int size, bool (*compare)(int, int))</code> — сортировку пузырьком на месте. Если <code>compare(a, b)</code> истинно, <code>a</code> должен идти раньше <code>b</code>. И компараторы <code>ascending</code>, <code>descending</code>.</p>',
 r'''bool ascending(int a, int b) { return a < b; }
bool descending(int a, int b) { return a > b; }
void bubbleSort(int* arr, int size, bool (*compare)(int, int)) {
    for (int i = 0; i < size; ++i)
        for (int j = 0; j + 1 < size - i; ++j)
            if (compare(arr[j + 1], arr[j])) { int t = arr[j]; arr[j] = arr[j + 1]; arr[j + 1] = t; }
}''', ['5\n3 1 4 1 5', '1\n9', '6\n-2 7 0 7 -9 3'], mode='func',
 starter='bool ascending(int a, int b) { return a < b; }\nbool descending(int a, int b) { return a > b; }\n\nvoid bubbleSort(int* arr, int size, bool (*compare)(int, int)) {\n    // TODO\n}\n',
 harness=r'''#include <iostream>
int main() {
    int n; std::cin >> n;
    int* a = new int[n];
    for (int i = 0; i < n; ++i) std::cin >> a[i];
    bubbleSort(a, n, ascending);
    for (int i = 0; i < n; ++i) std::cout << a[i] << ' ';
    std::cout << '\n';
    bubbleSort(a, n, descending);
    for (int i = 0; i < n; ++i) std::cout << a[i] << ' ';
    std::cout << '\n';
    delete[] a;
}''', inp='Массив.', out='По возрастанию и по убыванию.', check='tokens')

task('revarr', '16', 'Разворот массива на месте', 'easy', 'lc',
 '<p>LeetCode 344 (в версии для чисел). Разверни массив на месте двумя указателями, без второго массива, и выведи его.</p>',
 r'''#include <iostream>
int main() {
    int n; std::cin >> n;
    int* a = new int[n];
    for (int i = 0; i < n; ++i) std::cin >> a[i];
    for (int* l = a, *r = a + n - 1; l < r; ++l, --r) { int t = *l; *l = *r; *r = t; }
    for (int i = 0; i < n; ++i) std::cout << a[i] << (i + 1 < n ? " " : "\n");
    delete[] a;
}''', ['5\n1 2 3 4 5', '1\n7', '4\n4 3 2 1'], inp='<code>n</code> и массив.', out='Развёрнутый массив.', hint='Указатели <code>l</code> с начала и <code>r</code> с конца, меняем и сближаем, пока <code>l &lt; r</code> (сравнение указателей одного массива законно).')

task('twosum', '16', 'Two Sum', 'easy', 'lc',
 '<p>LeetCode 1. Дан массив и число <code>target</code>. Найди два <b>разных</b> индекса <code>i &lt; j</code> с <code>a[i] + a[j] == target</code> (гарантируется, что ответ ровно один) и выведи их. Решения за O(n²) достаточно.</p>',
 r'''#include <iostream>
int main() {
    int n, target; std::cin >> n >> target;
    int* a = new int[n];
    for (int i = 0; i < n; ++i) std::cin >> a[i];
    for (int i = 0; i < n; ++i)
        for (int j = i + 1; j < n; ++j)
            if (a[i] + a[j] == target) { std::cout << i << ' ' << j << '\n'; delete[] a; return 0; }
    delete[] a;
}''', ['4 9\n2 7 11 15', '3 6\n3 2 4', '2 6\n3 3', '5 -8\n-1 -2 -3 -4 -5'], inp='<code>n target</code>, затем массив.', out='<code>i j</code>')

task('movezero', '16', 'Сдвинуть нули в конец', 'easy', 'lc',
 '<p>LeetCode 283. Перемести все нули в конец массива, сохранив порядок ненулевых элементов. На месте, без второго массива.</p>',
 r'''#include <iostream>
int main() {
    int n; std::cin >> n;
    int* a = new int[n];
    for (int i = 0; i < n; ++i) std::cin >> a[i];
    int w = 0;
    for (int i = 0; i < n; ++i) if (a[i] != 0) a[w++] = a[i];
    while (w < n) a[w++] = 0;
    for (int i = 0; i < n; ++i) std::cout << a[i] << (i + 1 < n ? " " : "\n");
    delete[] a;
}''', ['5\n0 1 0 3 12', '1\n0', '3\n1 2 3', '4\n0 0 0 5'], inp='Массив.', out='Массив.', hint='Индекс записи <code>w</code>: проходим массив и пишем ненулевые в <code>a[w++]</code>, потом добиваем нулями.')

task('kadane', '16', 'Подмассив с максимальной суммой', 'medium', 'lc',
 '<p>LeetCode 53 «Maximum Subarray». Найди максимальную сумму непустого непрерывного подмассива за O(n) (алгоритм Кадане).</p>',
 r'''#include <iostream>
int main() {
    int n; std::cin >> n;
    long long best, cur = 0;
    for (int i = 0; i < n; ++i) {
        long long x; std::cin >> x;
        cur = cur > 0 ? cur + x : x;
        if (i == 0 || cur > best) best = cur;
    }
    std::cout << best << '\n';
}''', ['9\n-2 1 -3 4 -1 2 1 -5 4', '1\n1', '5\n5 4 -1 7 8', '3\n-3 -1 -2'], inp='Массив.', out='Сумма.', hint='Идём слева направо: если текущая сумма стала отрицательной, выгоднее начать заново с текущего элемента.')

task('dedup', '16', 'Удалить дубликаты из отсортированного', 'easy', 'lc',
 '<p>LeetCode 26. Массив отсортирован по неубыванию. Оставь каждое значение по одному разу (на месте) и выведи количество уникальных и их самих.</p>',
 r'''#include <iostream>
int main() {
    int n; std::cin >> n;
    int* a = new int[n];
    for (int i = 0; i < n; ++i) std::cin >> a[i];
    int k = n ? 1 : 0;
    for (int i = 1; i < n; ++i) if (a[i] != a[k - 1]) a[k++] = a[i];
    std::cout << k << '\n';
    for (int i = 0; i < k; ++i) std::cout << a[i] << (i + 1 < k ? " " : "");
    std::cout << '\n';
    delete[] a;
}''', ['3\n1 1 2', '10\n0 0 1 1 1 2 2 3 3 4', '1\n5'], inp='Массив.', out='<code>k</code>, затем уникальные.')

task('rotate', '16', 'Циклический сдвиг', 'medium', 'lc',
 '<p>LeetCode 189. Сдвинь массив вправо на <code>k</code> позиций (k может быть больше n). Можно решить за O(1) доп. памяти тремя разворотами.</p>',
 r'''#include <iostream>
void rev(int* l, int* r) { while (l < r) { int t = *l; *l++ = *r; *r-- = t; } }
int main() {
    int n, k; std::cin >> n >> k;
    int* a = new int[n];
    for (int i = 0; i < n; ++i) std::cin >> a[i];
    k %= n;
    if (k > 0) {
        rev(a, a + n - 1);
        rev(a, a + k - 1);
        rev(a + k, a + n - 1);
    }
    for (int i = 0; i < n; ++i) std::cout << a[i] << (i + 1 < n ? " " : "\n");
    delete[] a;
}''', ['7 3\n1 2 3 4 5 6 7', '4 2\n-1 -100 3 99', '3 10\n1 2 3', '1 5\n9'], inp='<code>n k</code>, массив.', out='Сдвинутый массив.', hint='Развернуть весь массив, потом первые k и оставшиеся n − k.')

# ======================= Глава 17: строки =======================
task('upper', '17', 'toUpperCase', 'easy', 'sem',
 '<p>Упражнение 8.1. Напиши <code>std::string toUpperCase(const std::string&amp; s)</code> — копия строки, где латинские буквы переведены в верхний регистр (<code>std::toupper</code> из <code>&lt;cctype&gt;</code>).</p>',
 r'''#include <string>
#include <cctype>
std::string toUpperCase(const std::string& s) {
    std::string r = s;
    for (char& c : r) c = static_cast<char>(std::toupper(static_cast<unsigned char>(c)));
    return r;
}''', ['Hello, World!', 'c++ is 2x Fun', '123'], mode='func', starter='#include <string>\n#include <cctype>\n\nstd::string toUpperCase(const std::string& s) {\n    // TODO\n}\n',
 harness=r'''#include <iostream>
int main() {
    std::string s; std::getline(std::cin, s);
    std::string u = toUpperCase(s);
    std::cout << u << '\n' << s << '\n';
}''', inp='Строка.', out='Строка в верхнем регистре и исходная (не должна измениться).')

task('countwords', '17', 'countWords', 'easy', 'sem',
 '<p>Упражнение 8.2. Напиши <code>size_t countWords(const std::string&amp; text)</code> — число слов (последовательностей непробельных символов). Используй <code>std::istringstream</code>.</p>',
 r'''#include <string>
#include <sstream>
size_t countWords(const std::string& text) {
    std::istringstream iss(text);
    std::string w;
    size_t c = 0;
    while (iss >> w) ++c;
    return c;
}''', ['hello world', '   many   spaces   here  ', '', 'one'], mode='func', starter='#include <string>\n#include <sstream>\n\nsize_t countWords(const std::string& text) {\n    // TODO\n}\n',
 harness=r'''#include <iostream>
int main() {
    std::string s; std::getline(std::cin, s);
    std::cout << countWords(s) << '\n';
}''', inp='Строка.', out='Число слов.')

task('removeall', '17', 'removeAll', 'medium', 'sem',
 '<p>Упражнение 8.3. Напиши <code>std::string removeAll(std::string s, const std::string&amp; substr)</code> — удаляет все вхождения <code>substr</code> циклом с <code>find</code> и <code>erase</code>. Подстрока непустая.</p>',
 r'''#include <string>
std::string removeAll(std::string s, const std::string& substr) {
    size_t pos;
    while ((pos = s.find(substr)) != std::string::npos) s.erase(pos, substr.size());
    return s;
}''', ['banana\nan', 'aaaa\naa', 'hello\nxyz', 'abcabcabc\nabc', 'aabb\nab'], mode='func', starter='#include <string>\n\nstd::string removeAll(std::string s, const std::string& substr) {\n    // TODO\n}\n',
 harness=r'''#include <iostream>
int main() {
    std::string s, t;
    std::getline(std::cin, s); std::getline(std::cin, t);
    std::cout << "[" << removeAll(s, t) << "]\n";
}''', inp='Строка и подстрока (по строке на каждую).', out='Результат в квадратных скобках.', hint='Каверзный тест — <code>aabb</code> без <code>ab</code>: после удаления появляется новое вхождение. Если искать заново с начала строки, это учтётся само.')

task('ispal', '17', 'isPalindrome(string_view)', 'easy', 'sem',
 '<p>Упражнение 8.4. Напиши <code>bool isPalindrome(std::string_view sv)</code>: читается ли строка одинаково с обеих сторон (с учётом всех символов и регистра).</p>',
 r'''#include <string_view>
bool isPalindrome(std::string_view sv) {
    if (sv.empty()) return true;
    for (size_t i = 0, j = sv.size() - 1; i < j; ++i, --j)
        if (sv[i] != sv[j]) return false;
    return true;
}''', ['level', 'abca', 'a', 'abba', 'Aa'], mode='func', starter='#include <string_view>\n\nbool isPalindrome(std::string_view sv) {\n    // TODO\n}\n',
 harness=r'''#include <iostream>
#include <string>
int main() {
    std::string s; std::getline(std::cin, s);
    std::cout << (isPalindrome(s) ? "YES" : "NO") << '\n';
}''', inp='Строка.', out='<code>YES</code>/<code>NO</code>', hint='Аккуратно с пустой строкой: <code>sv.size() - 1</code> для пустой — огромное беззнаковое число.')

task('validpal', '17', 'Valid Palindrome', 'medium', 'lc',
 '<p>LeetCode 125. Строка — палиндром, если после удаления всех не буквенно-цифровых символов и приведения к нижнему регистру она читается одинаково. Выведи <code>true</code>/<code>false</code>.</p>',
 r'''#include <iostream>
#include <string>
#include <cctype>
int main() {
    std::string s; std::getline(std::cin, s);
    int i = 0, j = (int)s.size() - 1;
    bool ok = true;
    while (i < j) {
        unsigned char a = s[i], b = s[j];
        if (!std::isalnum(a)) { ++i; continue; }
        if (!std::isalnum(b)) { --j; continue; }
        if (std::tolower(a) != std::tolower(b)) { ok = false; break; }
        ++i; --j;
    }
    std::cout << (ok ? "true" : "false") << '\n';
}''', ['A man, a plan, a canal: Panama', 'race a car', ' ', '0P'], inp='Строка.', out='<code>true</code>/<code>false</code>', starter=io_starter('#include <string>\n#include <cctype>\n'))

task('anagram', '17', 'Анаграммы', 'easy', 'lc',
 '<p>LeetCode 242. Даны две строки из строчных латинских букв. Выведи <code>true</code>, если одна — перестановка букв другой. Подсказка: массив из 26 счётчиков и <code>c - \'a\'</code>.</p>',
 r'''#include <iostream>
#include <string>
int main() {
    std::string s, t; std::cin >> s >> t;
    int cnt[26]{};
    for (char c : s) ++cnt[c - 'a'];
    for (char c : t) --cnt[c - 'a'];
    bool ok = s.size() == t.size();
    for (int i = 0; i < 26; ++i) if (cnt[i] != 0) ok = false;
    std::cout << (ok ? "true" : "false") << '\n';
}''', ['anagram nagaram', 'rat car', 'a a', 'ab abb'], inp='Две строки.', out='<code>true</code>/<code>false</code>', starter=io_starter('#include <string>\n'))

task('revwords', '17', 'Слова в обратном порядке', 'medium', 'lc',
 '<p>LeetCode 151. Выведи слова строки в обратном порядке, разделив их ровно одним пробелом (лишние пробелы по краям и между словами убрать).</p>',
 r'''#include <iostream>
#include <string>
#include <sstream>
int main() {
    std::string line; std::getline(std::cin, line);
    std::istringstream iss(line);
    std::string w, res;
    while (iss >> w) res = res.empty() ? w : w + " " + res;
    std::cout << res << '\n';
}''', ['the sky is blue', '  hello world  ', 'a good   example', 'one'], inp='Строка.', out='Слова в обратном порядке.', starter=io_starter('#include <string>\n#include <sstream>\n'))

task('firstuniq', '17', 'Первый неповторяющийся символ', 'easy', 'lc',
 '<p>LeetCode 387. Строка из строчных латинских букв. Выведи индекс первого символа, который встречается ровно один раз, или −1.</p>',
 r'''#include <iostream>
#include <string>
int main() {
    std::string s; std::cin >> s;
    int cnt[26]{};
    for (char c : s) ++cnt[c - 'a'];
    for (size_t i = 0; i < s.size(); ++i) if (cnt[s[i] - 'a'] == 1) { std::cout << i << '\n'; return 0; }
    std::cout << -1 << '\n';
}''', ['leetcode', 'loveleetcode', 'aabb', 'z'], inp='Строка.', out='Индекс или −1.', starter=io_starter('#include <string>\n'))

task('mystrlen', '17', 'Свой strlen', 'easy', 'lect',
 '<p>Напиши <code>size_t myStrlen(const char* s)</code> без <code>&lt;cstring&gt;</code>: длина C-строки — количество символов до терминала <code>\'\\0\'</code>. Используй арифметику указателей.</p>',
 r'''#include <cstddef>
size_t myStrlen(const char* s) {
    const char* p = s;
    while (*p != '\0') ++p;
    return p - s;
}''', ['hello', 'a', ''], mode='func', starter='#include <cstddef>\n\nsize_t myStrlen(const char* s) {\n    // TODO\n}\n',
 harness=r'''#include <iostream>
#include <string>
int main() {
    std::string s; std::getline(std::cin, s);
    char buf[100] = "abc\0def";
    std::cout << myStrlen(s.c_str()) << ' ' << myStrlen(buf) << '\n';
}''', inp='Строка.', out='Длина строки и длина <code>"abc\\0def"</code>.', hint='Двигай указатель, пока не встретишь <code>\'\\0\'</code>; разность указателей — это длина.')

task('roman', '17', 'Римские цифры', 'medium', 'lc',
 '<p>LeetCode 13. Переведи римское число (1..3999) в арабское. Если символ меньше следующего за ним (IV, IX, XL…), он вычитается.</p>',
 r'''#include <iostream>
#include <string>
int val(char c) {
    switch (c) {
        case 'I': return 1; case 'V': return 5; case 'X': return 10; case 'L': return 50;
        case 'C': return 100; case 'D': return 500; case 'M': return 1000;
    }
    return 0;
}
int main() {
    std::string s; std::cin >> s;
    int r = 0;
    for (size_t i = 0; i < s.size(); ++i) {
        int v = val(s[i]);
        if (i + 1 < s.size() && v < val(s[i + 1])) r -= v; else r += v;
    }
    std::cout << r << '\n';
}''', ['III', 'LVIII', 'MCMXCIV', 'IX', 'MMMCMXCIX'], inp='Римское число.', out='Арабское.', starter=io_starter('#include <string>\n'), hint='<code>switch</code> по символу для значения, и одно правило: вычитаем, если следующий символ больше.')

# ======================= Глава 18: файлы =======================
FILE_PRE = r'''#include <iostream>
#include <fstream>
#include <string>
static void prepare(const char* name) {
    std::ofstream f(name);
    std::string line;
    while (std::getline(std::cin, line)) f << line << '\n';
}'''
task('copyfile', '18', 'Копирование файла', 'easy', 'sem',
 '<p>Упражнение 8.5. Напиши <code>bool copyFile(const std::string&amp; from, const std::string&amp; to)</code>: копирует содержимое построчно, возвращает <code>false</code>, если исходный файл не открылся. Проверяющий main создаст файл из ввода и выведет копию.</p>',
 r'''#include <fstream>
#include <string>
bool copyFile(const std::string& from, const std::string& to) {
    std::ifstream in(from);
    if (!in.is_open()) return false;
    std::ofstream out(to);
    std::string line;
    while (std::getline(in, line)) out << line << '\n';
    return true;
}''', ['hello\nworld', 'single line', 'a\n\nb'], mode='func', starter='#include <fstream>\n#include <string>\n\nbool copyFile(const std::string& from, const std::string& to) {\n    // TODO\n}\n',
 harness=FILE_PRE + r'''
int main() {
    prepare("input.txt");
    std::cout << std::boolalpha << copyFile("input.txt", "copy.txt") << ' ' << copyFile("nope.txt", "x.txt") << '\n';
    std::ifstream c("copy.txt");
    std::string line;
    while (std::getline(c, line)) std::cout << line << '\n';
}''', inp='Содержимое исходного файла.', out='Результаты вызовов и содержимое копии.')

task('procnums', '18', 'Числа из файла и их квадраты', 'medium', 'sem',
 '<p>Упражнение 8.6. Напиши <code>void processNumbers(const std::string&amp; filename)</code>: читает файл построчно (<code>std::getline</code>); если строка — целое число (необязательный знак <code>-</code>/<code>+</code> и только цифры, не длиннее 9 цифр), выводит <code>число квадрат</code>, иначе пропускает строку. Проверь строку вручную до <code>std::stoi</code> (без <code>try</code>/<code>catch</code> — исключения будут во втором модуле): иначе <code>stoi("abc")</code> бросит исключение и программа упадёт.</p>',
 r'''#include <iostream>
#include <fstream>
#include <string>
static bool isInt(const std::string& s) {
    size_t i = 0;
    if (i < s.size() && (s[i] == '-' || s[i] == '+')) ++i;
    if (i == s.size() || s.size() - i > 9) return false;
    for (; i < s.size(); ++i) if (s[i] < '0' || s[i] > '9') return false;
    return true;
}
void processNumbers(const std::string& filename) {
    std::ifstream in(filename);
    std::string line;
    while (std::getline(in, line)) {
        if (!isInt(line)) continue;
        long long n = std::stoi(line);
        std::cout << n << ' ' << n * n << '\n';
    }
}''', ['5\nabc\n-12\n\n7x\n+3', '100\n200', 'none'], mode='func', starter='#include <iostream>\n#include <fstream>\n#include <string>\n\nvoid processNumbers(const std::string& filename) {\n    // TODO\n}\n',
 harness=FILE_PRE + r'''
int main() {
    prepare("nums.txt");
    processNumbers("nums.txt");
}''', inp='Строки файла.', out='Пары <code>число квадрат</code>.')

task('wcfile', '18', 'Мини-wc', 'medium', 'sem',
 '<p>Упражнение 8.7. Напиши <code>void stats(const std::string&amp; filename)</code>, выводящую в одной строке: количество символов (без символов перевода строки), количество строк и количество слов. Используй <code>std::getline</code> и <code>std::istringstream</code>.</p>',
 r'''#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
void stats(const std::string& filename) {
    std::ifstream in(filename);
    std::string line, w;
    long long chars = 0, lines = 0, words = 0;
    while (std::getline(in, line)) {
        ++lines;
        chars += line.size();
        std::istringstream iss(line);
        while (iss >> w) ++words;
    }
    std::cout << chars << ' ' << lines << ' ' << words << '\n';
}''', ['hello world\nsecond line here', 'one', 'a b c\n\n d '], mode='func', starter='#include <iostream>\n#include <fstream>\n#include <sstream>\n#include <string>\n\nvoid stats(const std::string& filename) {\n    // TODO\n}\n',
 harness=FILE_PRE + r'''
int main() {
    prepare("text.txt");
    stats("text.txt");
}''', inp='Строки файла.', out='<code>символы строки слова</code>')

task('replacefile', '18', 'Замена в файле', 'medium', 'sem',
 '<p>Упражнение 8.8. Напиши <code>void replaceInFile(const std::string&amp; filename, const std::string&amp; oldStr, const std::string&amp; newStr)</code>: читает весь файл в строку, заменяет все вхождения и перезаписывает файл. Аккуратно: если <code>newStr</code> содержит <code>oldStr</code>, поиск не должен зациклиться.</p>',
 r'''#include <fstream>
#include <sstream>
#include <string>
void replaceInFile(const std::string& filename, const std::string& oldStr, const std::string& newStr) {
    std::ifstream in(filename);
    std::stringstream ss;
    ss << in.rdbuf();
    in.close();
    std::string s = ss.str();
    size_t pos = 0;
    while ((pos = s.find(oldStr, pos)) != std::string::npos) {
        s.replace(pos, oldStr.size(), newStr);
        pos += newStr.size();
    }
    std::ofstream out(filename);
    out << s;
}''', ['cat\ncats\nthe cat sat on the cat', 'a\naa\nbanana', 'x\ny\nnothing here'], mode='func',
 starter='#include <fstream>\n#include <sstream>\n#include <string>\n\nvoid replaceInFile(const std::string& filename, const std::string& oldStr, const std::string& newStr) {\n    // TODO\n}\n',
 harness=r'''#include <iostream>
#include <fstream>
#include <string>
int main() {
    std::string o, n, line;
    std::getline(std::cin, o); std::getline(std::cin, n);
    { std::ofstream f("f.txt"); while (std::getline(std::cin, line)) f << line << '\n'; }
    replaceInFile("f.txt", o, n);
    std::ifstream f("f.txt");
    while (std::getline(f, line)) std::cout << line << '\n';
}''', inp='Первая строка — что заменить, вторая — на что, дальше — содержимое файла.', out='Файл после замены.', hint='После замены продолжай поиск с <code>pos + newStr.size()</code>.')

task('csv', '18', 'Разбор CSV', 'easy', 'sem',
 '<p>Упражнение 8.9. Напиши <code>void printCSV(const std::string&amp; filename)</code>. В каждой строке файла три поля <code>name,age,city</code>. Выводи <code>Name: Anna | Age: 25 | City: Moscow</code>. Для разбора используй <code>std::getline(iss, field, \',\')</code>.</p>',
 r'''#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
void printCSV(const std::string& filename) {
    std::ifstream in(filename);
    std::string line;
    while (std::getline(in, line)) {
        std::istringstream iss(line);
        std::string name, age, city;
        std::getline(iss, name, ',');
        std::getline(iss, age, ',');
        std::getline(iss, city);
        std::cout << "Name: " << name << " | Age: " << age << " | City: " << city << '\n';
    }
}''', ['Anna,25,Moscow\nIvan,30,St Petersburg\nOlga,28,Novosibirsk', 'Bob,1,X'], mode='func',
 starter='#include <iostream>\n#include <fstream>\n#include <sstream>\n#include <string>\n\nvoid printCSV(const std::string& filename) {\n    // TODO\n}\n',
 harness=FILE_PRE + r'''
int main() {
    prepare("data.csv");
    printCSV("data.csv");
}''', inp='Строки CSV.', out='Отформатированные строки.')

# ======================= Глава 19: матрицы =======================
MAT_READ = r'''#include <iostream>
int main() {
    int n, m; std::cin >> n >> m;
    int** a = new int*[n];
    for (int i = 0; i < n; ++i) { a[i] = new int[m]; for (int j = 0; j < m; ++j) std::cin >> a[i][j]; }
'''
MAT_FREE = r'''
    for (int i = 0; i < n; ++i) delete[] a[i];
    delete[] a;
}'''
task('diagsum', '19', 'Суммы диагоналей', 'easy', 'sem',
 '<p>Квадратная матрица n×n. Выведи сумму главной диагонали и сумму побочной через пробел.</p>',
 r'''#include <iostream>
int main() {
    int n; std::cin >> n;
    int a[20][20];
    for (int i = 0; i < n; ++i) for (int j = 0; j < n; ++j) std::cin >> a[i][j];
    long long d1 = 0, d2 = 0;
    for (int i = 0; i < n; ++i) { d1 += a[i][i]; d2 += a[i][n - 1 - i]; }
    std::cout << d1 << ' ' << d2 << '\n';
}''', ['3\n1 2 3\n4 5 6\n7 8 9', '1\n5', '2\n1 2\n3 4', '4\n1 0 0 2\n0 3 4 0\n0 5 6 0\n7 0 0 8'], inp='n (≤ 20), затем матрица.', out='Две суммы.')

task('issym', '19', 'Симметрична ли матрица', 'easy', 'sem',
 '<p>Напиши <code>bool isSymmetric(int** a, int n)</code>: <code>a[i][j] == a[j][i]</code> для всех i, j. Достаточно проверить элементы над диагональю.</p>',
 r'''bool isSymmetric(int** a, int n) {
    for (int i = 0; i < n; ++i)
        for (int j = i + 1; j < n; ++j)
            if (a[i][j] != a[j][i]) return false;
    return true;
}''', ['3 3\n1 2 3\n2 5 6\n3 6 9', '2 2\n1 2\n3 1', '1 1\n7'], mode='func',
 starter='bool isSymmetric(int** a, int n) {\n    // TODO\n}\n',
 harness=MAT_READ + '    std::cout << std::boolalpha << isSymmetric(a, n) << \'\\n\';' + MAT_FREE, inp='n n, затем матрица.', out='<code>true</code>/<code>false</code>')

task('transpose', '19', 'Транспонирование', 'easy', 'sem',
 '<p>Напиши <code>int** transpose(int** a, int rows, int cols)</code>, которая выделяет новую матрицу cols×rows и заполняет её транспонированной. Исходную не трогай; освобождать результат будет вызывающий.</p>',
 r'''int** transpose(int** a, int rows, int cols) {
    int** t = new int*[cols];
    for (int j = 0; j < cols; ++j) {
        t[j] = new int[rows];
        for (int i = 0; i < rows; ++i) t[j][i] = a[i][j];
    }
    return t;
}''', ['2 3\n1 2 3\n4 5 6', '1 4\n1 2 3 4', '3 1\n7\n8\n9'], mode='func',
 starter='int** transpose(int** a, int rows, int cols) {\n    // TODO\n}\n',
 harness=MAT_READ + r'''    int** t = transpose(a, n, m);
    for (int j = 0; j < m; ++j) { for (int i = 0; i < n; ++i) std::cout << t[j][i] << ' '; std::cout << '\n'; }
    for (int j = 0; j < m; ++j) delete[] t[j];
    delete[] t;''' + MAT_FREE, inp='rows cols, затем матрица.', out='Транспонированная матрица.')

task('matmax', '19', 'Максимум и его позиция', 'easy', 'sem',
 '<p>Найди максимальный элемент матрицы n×m и его позицию (первое вхождение при обходе по строкам). Выведи <code>max i j</code>.</p>',
 r'''#include <iostream>
int main() {
    int n, m; std::cin >> n >> m;
    int best = 0, bi = -1, bj = -1;
    for (int i = 0; i < n; ++i) for (int j = 0; j < m; ++j) {
        int x; std::cin >> x;
        if (bi == -1 || x > best) { best = x; bi = i; bj = j; }
    }
    std::cout << best << ' ' << bi << ' ' << bj << '\n';
}''', ['2 3\n1 9 3\n4 9 6', '1 1\n-5', '3 2\n-1 -2\n-3 -4\n-5 -1'], inp='n m, матрица.', out='<code>max i j</code>')

task('snake', '19', 'Змейка', 'medium', 'sem',
 '<p>Заполни матрицу n×m числами 1, 2, 3… «змейкой»: чётные строки (с нуля) слева направо, нечётные — справа налево. Выведи её, разделяя числа пробелом.</p>',
 r'''#include <iostream>
int main() {
    int n, m; std::cin >> n >> m;
    int a[20][20], k = 1;
    for (int i = 0; i < n; ++i)
        for (int j = 0; j < m; ++j)
            a[i][i % 2 == 0 ? j : m - 1 - j] = k++;
    for (int i = 0; i < n; ++i) { for (int j = 0; j < m; ++j) std::cout << (j ? " " : "") << a[i][j]; std::cout << '\n'; }
}''', ['3 4', '1 5', '4 1', '2 2'], inp='n m (≤ 20).', out='Матрица.')

task('spiral', '19', 'Спиральная матрица', 'medium', 'lc',
 '<p>LeetCode 59 (вариант n×m). Заполни матрицу числами 1…n·m по спирали по часовой стрелке, начиная с левого верхнего угла. Числа через пробел.</p>',
 r'''#include <iostream>
int main() {
    int n, m; std::cin >> n >> m;
    int a[20][20], k = 1;
    int top = 0, bot = n - 1, l = 0, r = m - 1;
    while (top <= bot && l <= r) {
        for (int j = l; j <= r; ++j) a[top][j] = k++;
        ++top;
        for (int i = top; i <= bot; ++i) a[i][r] = k++;
        --r;
        if (top <= bot) { for (int j = r; j >= l; --j) a[bot][j] = k++; --bot; }
        if (l <= r) { for (int i = bot; i >= top; --i) a[i][l] = k++; ++l; }
    }
    for (int i = 0; i < n; ++i) { for (int j = 0; j < m; ++j) std::cout << (j ? " " : "") << a[i][j]; std::cout << '\n'; }
}''', ['3 3', '3 4', '1 4', '4 1', '4 4'], inp='n m (≤ 20).', out='Матрица.', hint='Держи четыре границы (top, bottom, left, right) и сдвигай их после каждой стороны. Проверки <code>top &lt;= bottom</code> и <code>left &lt;= right</code> перед обратными проходами спасают от повторов на узких матрицах.')

task('spiralccw', '19', 'Спираль против часовой', 'medium', 'sem',
 '<p>Вариант с семинара: заполни квадратную матрицу n×n числами 1…n² по спирали <b>против</b> часовой стрелки, начиная с левого верхнего угла (сначала вниз по левому столбцу).</p>',
 r'''#include <iostream>
int main() {
    int n; std::cin >> n;
    int a[20][20], k = 1;
    int top = 0, bot = n - 1, l = 0, r = n - 1;
    while (top <= bot && l <= r) {
        for (int i = top; i <= bot; ++i) a[i][l] = k++;
        ++l;
        for (int j = l; j <= r; ++j) a[bot][j] = k++;
        --bot;
        if (l <= r) { for (int i = bot; i >= top; --i) a[i][r] = k++; --r; }
        if (top <= bot) { for (int j = r; j >= l; --j) a[top][j] = k++; ++top; }
    }
    for (int i = 0; i < n; ++i) { for (int j = 0; j < n; ++j) std::cout << (j ? " " : "") << a[i][j]; std::cout << '\n'; }
}''', ['3', '4', '1', '2'], inp='n (≤ 20).', out='Матрица.')

task('zerorows', '19', 'Строки с нулями', 'easy', 'sem',
 '<p>Для каждой строки матрицы n×m выведи количество нулей в ней, а последней строкой — номер строки (с нуля) с наибольшим числом нулей (первую при равенстве).</p>',
 r'''#include <iostream>
int main() {
    int n, m; std::cin >> n >> m;
    int best = -1, bi = 0;
    for (int i = 0; i < n; ++i) {
        int c = 0;
        for (int j = 0; j < m; ++j) { int x; std::cin >> x; if (x == 0) ++c; }
        std::cout << c << '\n';
        if (c > best) { best = c; bi = i; }
    }
    std::cout << bi << '\n';
}''', ['3 3\n0 1 0\n1 1 1\n0 0 0', '2 2\n1 2\n3 4'], inp='n m, матрица.', out='Счётчики и номер строки.')

task('rotate90', '19', 'Поворот на 90°', 'medium', 'lc',
 '<p>LeetCode 48. Поверни квадратную матрицу на 90° по часовой стрелке <b>на месте</b>: транспонируй, затем разверни каждую строку.</p>',
 r'''#include <iostream>
#include <utility>
int main() {
    int n; std::cin >> n;
    int a[20][20];
    for (int i = 0; i < n; ++i) for (int j = 0; j < n; ++j) std::cin >> a[i][j];
    for (int i = 0; i < n; ++i) for (int j = i + 1; j < n; ++j) std::swap(a[i][j], a[j][i]);
    for (int i = 0; i < n; ++i) for (int j = 0; j < n / 2; ++j) std::swap(a[i][j], a[i][n - 1 - j]);
    for (int i = 0; i < n; ++i) { for (int j = 0; j < n; ++j) std::cout << (j ? " " : "") << a[i][j]; std::cout << '\n'; }
}''', ['3\n1 2 3\n4 5 6\n7 8 9', '2\n1 2\n3 4', '1\n5'], inp='n, матрица.', out='Повёрнутая матрица.')

task('pascal', '19', 'Треугольник Паскаля', 'easy', 'lc',
 '<p>LeetCode 118. Выведи первые n строк треугольника Паскаля. Храни их в «рваном» массиве: строка i — <code>new long long[i + 1]</code>.</p>',
 r'''#include <iostream>
int main() {
    int n; std::cin >> n;
    long long** t = new long long*[n];
    for (int i = 0; i < n; ++i) {
        t[i] = new long long[i + 1];
        t[i][0] = t[i][i] = 1;
        for (int j = 1; j < i; ++j) t[i][j] = t[i - 1][j - 1] + t[i - 1][j];
        for (int j = 0; j <= i; ++j) std::cout << (j ? " " : "") << t[i][j];
        std::cout << '\n';
    }
    for (int i = 0; i < n; ++i) delete[] t[i];
    delete[] t;
}''', ['5', '1', '10'], inp='n (1..30).', out='n строк.')

task('mateq', '19', 'Равны ли матрицы', 'easy', 'sem',
 '<p>Напиши <code>bool isEqual(int** a, int** b, int rows, int cols)</code>.</p>',
 r'''bool isEqual(int** a, int** b, int rows, int cols) {
    for (int i = 0; i < rows; ++i)
        for (int j = 0; j < cols; ++j)
            if (a[i][j] != b[i][j]) return false;
    return true;
}''', ['2 2\n1 2\n3 4\n1 2\n3 4', '2 3\n1 2 3\n4 5 6\n1 2 3\n4 5 7'], mode='func',
 starter='bool isEqual(int** a, int** b, int rows, int cols) {\n    // TODO\n}\n',
 harness=r'''#include <iostream>
int** readM(int n, int m) {
    int** a = new int*[n];
    for (int i = 0; i < n; ++i) { a[i] = new int[m]; for (int j = 0; j < m; ++j) std::cin >> a[i][j]; }
    return a;
}
void freeM(int** a, int n) { for (int i = 0; i < n; ++i) delete[] a[i]; delete[] a; }
int main() {
    int n, m; std::cin >> n >> m;
    int** a = readM(n, m); int** b = readM(n, m);
    std::cout << std::boolalpha << isEqual(a, b, n, m) << ' ' << isEqual(a, a, n, m) << '\n';
    freeM(a, n); freeM(b, n);
}''', inp='n m, затем две матрицы.', out='Два результата.')

task('matfile', '19', 'Матрица из файла', 'medium', 'sem',
 '<p>Напиши <code>int** readMatrixFromFile(const std::string&amp; filename, int&amp; rows, int&amp; cols)</code>: в файле сначала rows и cols, затем элементы. Если файл не открылся — верни <code>nullptr</code>.</p>',
 r'''#include <fstream>
#include <string>
int** readMatrixFromFile(const std::string& filename, int& rows, int& cols) {
    std::ifstream in(filename);
    if (!in.is_open()) return nullptr;
    in >> rows >> cols;
    int** a = new int*[rows];
    for (int i = 0; i < rows; ++i) {
        a[i] = new int[cols];
        for (int j = 0; j < cols; ++j) in >> a[i][j];
    }
    return a;
}''', ['2 3\n1 2 3\n4 5 6', '1 1\n42'], mode='func',
 starter='#include <fstream>\n#include <string>\n\nint** readMatrixFromFile(const std::string& filename, int& rows, int& cols) {\n    // TODO\n}\n',
 harness=FILE_PRE + r'''
int main() {
    prepare("m.txt");
    int r = 0, c = 0;
    std::cout << (readMatrixFromFile("missing.txt", r, c) == nullptr ? "null" : "??") << '\n';
    int** a = readMatrixFromFile("m.txt", r, c);
    long long s = 0;
    for (int i = 0; i < r; ++i) for (int j = 0; j < c; ++j) s += a[i][j];
    std::cout << r << 'x' << c << " sum=" << s << " last=" << a[r - 1][c - 1] << '\n';
    for (int i = 0; i < r; ++i) delete[] a[i];
    delete[] a;
}''', inp='Содержимое файла.', out='Проверка nullptr и сводка.')

# ======================= Глава 20: структуры =======================
task('points', '20', 'Ближайшая к началу координат точка', 'easy', 'lect',
 '<p>Объяви <code>struct Point { double x, y; };</code> Считай n точек в массив структур и выведи ту, что ближе всего к (0, 0), в формате <code>(x, y)</code> (первую при равенстве). Сравнивай квадраты расстояний — корень не нужен.</p>',
 r'''#include <iostream>
struct Point { double x, y; };
int main() {
    int n; std::cin >> n;
    Point* p = new Point[n];
    for (int i = 0; i < n; ++i) std::cin >> p[i].x >> p[i].y;
    int b = 0;
    for (int i = 1; i < n; ++i)
        if (p[i].x * p[i].x + p[i].y * p[i].y < p[b].x * p[b].x + p[b].y * p[b].y) b = i;
    std::cout << '(' << p[b].x << ", " << p[b].y << ")\n";
    delete[] p;
}''', ['3\n3 4\n-1 1\n5 0', '1\n0 0', '2\n1.5 -2\n-1.5 2'], inp='n, затем n пар x y.', out='Точка.', starter=io_starter('\nstruct Point {\n    double x, y;\n};\n'))

task('vecsum', '20', 'Сумма векторов через структуру', 'easy', 'lect',
 '<p>Объяви <code>struct Vec2 { int x, y; };</code> и функции <code>Vec2 add(Vec2 a, Vec2 b)</code> и <code>int dot(const Vec2&amp; a, const Vec2&amp; b)</code>.</p>',
 r'''struct Vec2 { int x, y; };
Vec2 add(Vec2 a, Vec2 b) { return {a.x + b.x, a.y + b.y}; }
int dot(const Vec2& a, const Vec2& b) { return a.x * b.x + a.y * b.y; }''', ['1 2 3 4', '0 0 5 -5', '-1 3 2 7'], mode='func',
 starter='struct Vec2 {\n    int x, y;\n};\n\nVec2 add(Vec2 a, Vec2 b) {\n    // TODO\n}\n\nint dot(const Vec2& a, const Vec2& b) {\n    // TODO\n}\n',
 harness=r'''#include <iostream>
int main() {
    Vec2 a, b; std::cin >> a.x >> a.y >> b.x >> b.y;
    Vec2 s = add(a, b);
    std::cout << s.x << ' ' << s.y << ' ' << dot(a, b) << '\n';
}''', inp='Две пары координат.', out='Сумма и скалярное произведение.')

task('students', '20', 'Лучший студент', 'medium', 'lect',
 '<p>Объяви <code>struct Student { std::string name; int grades[3]; };</code> Считай n студентов (имя и три оценки) и выведи имя студента с наибольшим средним и это среднее с двумя знаками после запятой (первого при равенстве).</p>',
 r'''#include <iostream>
#include <iomanip>
#include <string>
struct Student { std::string name; int grades[3]; };
double avg(const Student& s) { return (s.grades[0] + s.grades[1] + s.grades[2]) / 3.0; }
int main() {
    int n; std::cin >> n;
    Student* st = new Student[n];
    for (int i = 0; i < n; ++i) std::cin >> st[i].name >> st[i].grades[0] >> st[i].grades[1] >> st[i].grades[2];
    int b = 0;
    for (int i = 1; i < n; ++i) if (avg(st[i]) > avg(st[b])) b = i;
    std::cout << st[b].name << ' ' << std::fixed << std::setprecision(2) << avg(st[b]) << '\n';
    delete[] st;
}''', ['3\nAnna 8 9 10\nIvan 10 10 6\nOlga 7 7 7', '1\nDanila 10 9 9'], inp='n, затем строки <code>имя o1 o2 o3</code>.', out='<code>имя среднее</code>', starter=io_starter('#include <iomanip>\n#include <string>\n\nstruct Student {\n    std::string name;\n    int grades[3];\n};\n'))

task('sortpts', '20', 'Сортировка точек', 'medium', 'lect',
 '<p>Отсортируй n точек <code>struct Point { int x, y; };</code> по возрастанию x, при равных x — по убыванию y. Используй <code>std::sort</code> с лямбдой-компаратором.</p>',
 r'''#include <iostream>
#include <algorithm>
struct Point { int x, y; };
int main() {
    int n; std::cin >> n;
    Point* p = new Point[n];
    for (int i = 0; i < n; ++i) std::cin >> p[i].x >> p[i].y;
    std::sort(p, p + n, [](const Point& a, const Point& b) { return a.x != b.x ? a.x < b.x : a.y > b.y; });
    for (int i = 0; i < n; ++i) std::cout << p[i].x << ' ' << p[i].y << '\n';
    delete[] p;
}''', ['4\n2 1\n1 5\n2 3\n1 7', '1\n0 0', '3\n5 5\n5 6\n-1 0'], inp='n, точки.', out='Точки по строкам.', starter=io_starter('#include <algorithm>\n\nstruct Point {\n    int x, y;\n};\n'))

task('dist2', '20', 'Расстояние между точками', 'easy', 'sem',
 '<p>Упражнение 10.1. Структура <code>Point { double x, y; }</code>. Считай две точки, выведи расстояние между ними с 3 знаками после запятой, затем точку, которая дальше от начала координат, в формате <code>(x, y)</code> (при равенстве — первую).</p>',
 r'''#include <iostream>
#include <iomanip>
#include <cmath>
struct Point { double x, y; };
double dist(const Point& a, const Point& b) { return std::sqrt((a.x - b.x) * (a.x - b.x) + (a.y - b.y) * (a.y - b.y)); }
int main() {
    Point p1, p2; std::cin >> p1.x >> p1.y >> p2.x >> p2.y;
    std::cout << std::fixed << std::setprecision(3) << dist(p1, p2) << '\n';
    Point o{0, 0};
    const Point& far = dist(p2, o) > dist(p1, o) ? p2 : p1;
    std::cout << std::defaultfloat << '(' << far.x << ", " << far.y << ")\n";
}''', ['0 0 3 4', '1 1 -2 -2', '5 0 0 5'], inp='x1 y1 x2 y2', out='Расстояние и дальняя точка.', starter=io_starter('#include <iomanip>\n#include <cmath>\n\nstruct Point {\n    double x, y;\n};\n'), hint='После <code>std::fixed</code> вернуть обычный формат можно манипулятором <code>std::defaultfloat</code>.')

# ======================= Глава 22: классы =======================
task('stackcls', '22', 'Класс Stack', 'medium', 'lect',
 '<p>Реализуй класс из лекции: <code>class Stack</code> на статическом массиве <code>int buffer_[kCapacity]</code> (<code>static const size_t kCapacity = 100</code>) с методами <code>void Push(int)</code>, <code>void Pop()</code>, <code>int Top() const</code>, <code>size_t Size() const</code>, <code>bool Empty() const</code>. Поля — приватные. Push в полный стек и Pop из пустого ничего не делают.</p>',
 r'''#include <cstddef>
class Stack {
public:
    void Push(int x) { if (size_ < kCapacity) buffer_[size_++] = x; }
    void Pop() { if (size_ > 0) --size_; }
    int Top() const { return buffer_[size_ - 1]; }
    size_t Size() const { return size_; }
    bool Empty() const { return size_ == 0; }
private:
    static const size_t kCapacity = 100;
    int buffer_[kCapacity];
    size_t size_ = 0;
};''', ['push 1\npush 2\ntop\nsize\npop\ntop\npop\nempty\npop\nsize', 'empty\npush 5\nempty\ntop', 'many'], mode='func',
 starter='#include <cstddef>\n\nclass Stack {\npublic:\n    void Push(int x);\n    void Pop();\n    int Top() const;\n    size_t Size() const;\n    bool Empty() const;\nprivate:\n    static const size_t kCapacity = 100;\n    int buffer_[kCapacity];\n    size_t size_ = 0;\n};\n\n// реализуй методы здесь или прямо в классе\n',
 harness=r'''#include <iostream>
#include <string>
int main() {
    Stack s;
    std::string cmd;
    while (std::cin >> cmd) {
        if (cmd == "push") { int x; std::cin >> x; s.Push(x); }
        else if (cmd == "pop") s.Pop();
        else if (cmd == "top") std::cout << s.Top() << '\n';
        else if (cmd == "size") std::cout << s.Size() << '\n';
        else if (cmd == "empty") std::cout << (s.Empty() ? "yes" : "no") << '\n';
        else if (cmd == "many") { for (int i = 0; i < 150; ++i) s.Push(i); std::cout << s.Size() << ' ' << s.Top() << '\n'; }
    }
    const Stack& cs = s;
    std::cout << "const size: " << cs.Size() << '\n';
}''', inp='Команды <code>push x</code>, <code>pop</code>, <code>top</code>, <code>size</code>, <code>empty</code>.', out='Ответы на запросы.', hint='Методы, которые не меняют объект, обязаны быть <code>const</code> — проверяющий код вызывает <code>Size()</code> у константной ссылки.')

task('minstack', '22', 'Min Stack', 'medium', 'lc',
 '<p>LeetCode 155. Реализуй класс <code>MinStack</code> с методами <code>push(int)</code>, <code>pop()</code>, <code>top()</code>, <code>getMin()</code> — все за O(1). Не более 10⁴ элементов; вызовы корректны (pop/top/getMin не вызываются у пустого стека). Используй два массива: значения и «минимум на момент вставки».</p>',
 r'''class MinStack {
public:
    void push(int x) {
        val_[n_] = x;
        mn_[n_] = (n_ == 0 || x < mn_[n_ - 1]) ? x : mn_[n_ - 1];
        ++n_;
    }
    void pop() { --n_; }
    int top() const { return val_[n_ - 1]; }
    int getMin() const { return mn_[n_ - 1]; }
private:
    int val_[10000];
    int mn_[10000];
    int n_ = 0;
};''', ['push -2\npush 0\npush -3\nmin\npop\ntop\nmin', 'push 5\npush 5\npush 3\npop\nmin\npop\nmin\ntop', 'push 1\npush 2\npush 0\nmin\npop\nmin'], mode='func',
 starter='class MinStack {\npublic:\n    void push(int x) {}\n    void pop() {}\n    int top() const { return 0; }\n    int getMin() const { return 0; }\nprivate:\n    // поля\n};\n',
 harness=r'''#include <iostream>
#include <string>
int main() {
    MinStack s;
    std::string c;
    while (std::cin >> c) {
        if (c == "push") { int x; std::cin >> x; s.push(x); }
        else if (c == "pop") s.pop();
        else if (c == "top") std::cout << s.top() << '\n';
        else if (c == "min") std::cout << s.getMin() << '\n';
    }
}''', inp='Команды.', out='Ответы <code>top</code>/<code>min</code>.')

# ======================= Глава 23–25: конструкторы, деструкторы, RAII =======================
task('date', '23', 'Структура Date', 'easy', 'sem',
 '<p>Упражнение 11.1. <code>struct Date</code> с полями <code>day, month, year</code>. Конструктор по умолчанию — 01.01.1970, конструктор с тремя параметрами, метод <code>void print() const</code> (формат <code>DD.MM.YYYY</code>, с ведущими нулями) и <code>bool isLeapYear() const</code>.</p>',
 r'''#include <iostream>
#include <iomanip>
struct Date {
    int day, month, year;
    Date() : day(1), month(1), year(1970) {}
    Date(int d, int m, int y) : day(d), month(m), year(y) {}
    void print() const {
        std::cout << std::setfill('0') << std::setw(2) << day << '.' << std::setw(2) << month << '.'
                  << std::setw(4) << year << std::setfill(' ');
    }
    bool isLeapYear() const { return year % 400 == 0 || (year % 4 == 0 && year % 100 != 0); }
};''', ['5 3 2024', '31 12 1900', '29 2 2000'], mode='func',
 starter='#include <iostream>\n#include <iomanip>\n\nstruct Date {\n    int day, month, year;\n    // конструкторы, print(), isLeapYear()\n};\n',
 harness=r'''int main() {
    Date a;
    int d, m, y; std::cin >> d >> m >> y;
    Date b(d, m, y);
    const Date c{d, m, y};
    a.print(); std::cout << ' ' << a.isLeapYear() << '\n';
    b.print(); std::cout << ' ' << b.isLeapYear() << '\n';
    c.print(); std::cout << '\n';
}''', inp='d m y', out='Дата по умолчанию и введённая.', hint='<code>std::setfill(\'0\') &lt;&lt; std::setw(2)</code>. <code>setw</code> действует на один вывод, <code>setfill</code> — пока не сбросишь.')

task('counter', '24', 'Логирующий Counter', 'easy', 'sem',
 '<p>Упражнение 11.2. <code>struct Counter</code>: конструктор печатает <code>Counter()</code>, деструктор — <code>destr Counter()</code>, <code>void increment()</code> увеличивает значение и печатает его, <code>int getValue() const</code> возвращает значение без вывода. Каждое сообщение — на отдельной строке. Проверяющий код создаёт объекты в разных областях видимости — следи за порядком.</p>',
 r'''#include <iostream>
struct Counter {
    int value = 0;
    Counter() { std::cout << "Counter()\n"; }
    ~Counter() { std::cout << "destr Counter()\n"; }
    void increment() { ++value; std::cout << value << '\n'; }
    int getValue() const { return value; }
};''', ['2', '0'], mode='func',
 starter='#include <iostream>\n\nstruct Counter {\n    // TODO\n};\n',
 harness=r'''int main() {
    int k; std::cin >> k;
    Counter a;
    {
        Counter b;
        for (int i = 0; i < k; ++i) b.increment();
        std::cout << "inner " << b.getValue() << '\n';
    }
    const Counter c;
    std::cout << "const " << c.getValue() << '\n';
    a.increment();
    std::cout << "end of main\n";
}''', inp='Сколько раз увеличить внутренний счётчик.', out='Журнал вызовов.', hint='Объекты уничтожаются в порядке, обратном созданию, при выходе из своего блока.')

task('rect', '23', 'Прямоугольники', 'medium', 'sem',
 '<p>Упражнение 11.3. <code>struct Rectangle { int x, y, width, height; }</code> и функции <code>area</code>, <code>perimeter</code>, <code>move(Rectangle&amp;, int dx, int dy)</code>, <code>intersection</code> (если пересечения нет — прямоугольник нулевой площади: верни <code>{0, 0, 0, 0}</code>). Пересечение есть, если <code>max(a.x, b.x) &lt; min(a.x + a.width, b.x + b.width)</code> и аналогично по y.</p>',
 r'''#include <algorithm>
struct Rectangle { int x, y, width, height; };
int area(const Rectangle& r) { return r.width * r.height; }
int perimeter(const Rectangle& r) { return 2 * (r.width + r.height); }
void move(Rectangle& r, int dx, int dy) { r.x += dx; r.y += dy; }
Rectangle intersection(const Rectangle& a, const Rectangle& b) {
    int x1 = std::max(a.x, b.x), x2 = std::min(a.x + a.width, b.x + b.width);
    int y1 = std::max(a.y, b.y), y2 = std::min(a.y + a.height, b.y + b.height);
    if (x1 < x2 && y1 < y2) return {x1, y1, x2 - x1, y2 - y1};
    return {0, 0, 0, 0};
}''', ['0 0 4 3\n2 1 5 5\n1 1', '0 0 2 2\n5 5 1 1\n-5 -5', '0 0 10 10\n2 2 3 3\n0 0'], mode='func',
 starter='#include <algorithm>\n\nstruct Rectangle {\n    int x, y, width, height;\n};\n\nint area(const Rectangle& r);\nint perimeter(const Rectangle& r);\nvoid move(Rectangle& r, int dx, int dy);\nRectangle intersection(const Rectangle& a, const Rectangle& b);\n',
 harness=r'''#include <iostream>
void show(const Rectangle& r) { std::cout << r.x << ' ' << r.y << ' ' << r.width << ' ' << r.height << '\n'; }
int main() {
    Rectangle a, b; int dx, dy;
    std::cin >> a.x >> a.y >> a.width >> a.height >> b.x >> b.y >> b.width >> b.height >> dx >> dy;
    std::cout << area(a) << ' ' << perimeter(a) << '\n';
    Rectangle i = intersection(a, b);
    show(i); std::cout << area(i) << '\n';
    move(b, dx, dy); show(b);
    show(intersection(a, b));
}''', inp='Два прямоугольника и сдвиг.', out='Площадь, периметр, пересечения.')

task('products', '25', 'Товары и алгоритмы STL', 'medium', 'sem',
 '<p>Упражнение 11.4/12.1. <code>struct Product { std::string name; int price; int quantity; }</code> с конструктором. Реализуй с лямбдами: <code>sortByPrice</code>, <code>sortByName</code> (используй <code>std::stable_sort</code>, чтобы равные остались в исходном порядке), <code>filterCheaperThan</code> (строго дешевле), <code>totalCost</code> (Σ цена·количество, тип <code>long long</code>).</p>',
 r'''#include <string>
#include <vector>
#include <algorithm>
struct Product {
    std::string name; int price; int quantity;
    Product(std::string n, int p, int q) : name(n), price(p), quantity(q) {}
};
void sortByPrice(std::vector<Product>& v) { std::stable_sort(v.begin(), v.end(), [](const Product& a, const Product& b) { return a.price < b.price; }); }
void sortByName(std::vector<Product>& v) { std::stable_sort(v.begin(), v.end(), [](const Product& a, const Product& b) { return a.name < b.name; }); }
std::vector<Product> filterCheaperThan(const std::vector<Product>& v, int maxPrice) {
    std::vector<Product> r;
    std::copy_if(v.begin(), v.end(), std::back_inserter(r), [maxPrice](const Product& p) { return p.price < maxPrice; });
    return r;
}
long long totalCost(const std::vector<Product>& v) {
    long long s = 0;
    for (const auto& p : v) s += 1LL * p.price * p.quantity;
    return s;
}''', ['5\nmilk 8999 10\nbread 4500 20\ncheese 52000 3\napple 4500 100\ntea 19900 7\n10000', '1\nx 1 1\n1'], mode='func',
 starter='#include <string>\n#include <vector>\n#include <algorithm>\n\nstruct Product {\n    std::string name;\n    int price;\n    int quantity;\n    // конструктор\n};\n\nvoid sortByPrice(std::vector<Product>& v);\nvoid sortByName(std::vector<Product>& v);\nstd::vector<Product> filterCheaperThan(const std::vector<Product>& v, int maxPrice);\nlong long totalCost(const std::vector<Product>& v);\n',
 harness=r'''#include <iostream>
void show(const std::vector<Product>& v) { for (const auto& p : v) std::cout << p.name << ':' << p.price << ' '; std::cout << '\n'; }
int main() {
    int n; std::cin >> n;
    std::vector<Product> v;
    for (int i = 0; i < n; ++i) { std::string s; int p, q; std::cin >> s >> p >> q; v.emplace_back(s, p, q); }
    int mx; std::cin >> mx;
    std::cout << totalCost(v) << '\n';
    sortByPrice(v); show(v);
    sortByName(v); show(v);
    show(filterCheaperThan(v, mx));
}''', inp='n, товары, порог цены.', out='Итог, две сортировки, фильтр.')

task('intarray', '25', 'IntArray и правило трёх', 'hard', 'lect',
 '<p>Класс-владелец динамического массива: <code>IntArray(size_t n)</code> (нули), конструктор копирования (глубокая копия), оператор присваивания (copy-and-swap или с проверкой на самоприсваивание), деструктор, <code>int&amp; operator[](size_t)</code> + const-версия, <code>size_t size() const</code>. Проверяющий код копирует, присваивает, делает <code>a = a</code> и проверяет, что копии независимы.</p>',
 r'''#include <cstddef>
#include <utility>
class IntArray {
public:
    explicit IntArray(size_t n) : data_(new int[n]{}), size_(n) {}
    IntArray(const IntArray& o) : data_(new int[o.size_]), size_(o.size_) {
        for (size_t i = 0; i < size_; ++i) data_[i] = o.data_[i];
    }
    IntArray& operator=(const IntArray& o) {
        if (this != &o) {
            IntArray tmp(o);
            std::swap(data_, tmp.data_);
            std::swap(size_, tmp.size_);
        }
        return *this;
    }
    ~IntArray() { delete[] data_; }
    int& operator[](size_t i) { return data_[i]; }
    const int& operator[](size_t i) const { return data_[i]; }
    size_t size() const { return size_; }
private:
    int* data_;
    size_t size_;
};''', ['3\n1 2 3', '1\n42', '5\n5 4 3 2 1'], mode='func',
 starter='#include <cstddef>\n#include <utility>\n\nclass IntArray {\npublic:\n    explicit IntArray(size_t n);\n    IntArray(const IntArray& other);\n    IntArray& operator=(const IntArray& other);\n    ~IntArray();\n    int& operator[](size_t i);\n    const int& operator[](size_t i) const;\n    size_t size() const;\nprivate:\n    int* data_;\n    size_t size_;\n};\n',
 harness=r'''#include <iostream>
void show(const IntArray& a) { for (size_t i = 0; i < a.size(); ++i) std::cout << a[i] << ' '; std::cout << '\n'; }
int main() {
    size_t n; std::cin >> n;
    IntArray a(n);
    for (size_t i = 0; i < n; ++i) std::cin >> a[i];
    IntArray b = a;
    b[0] = -1;
    show(a); show(b);
    IntArray c(1);
    c = a;
    a[n - 1] = 100;
    show(c); show(a);
    IntArray& self = a;
    a = self;
    show(a);
    {
        IntArray d(2);
        d = b;
        show(d);
    }
    std::cout << "ok\n";
}''', inp='n и элементы.', out='Состояния массивов.', hint='Поверхностная копия (копируется указатель) даст общий буфер и двойной <code>delete[]</code> — именно это рисует трассировщик в главе 23.')

# ======================= Глава 26: перегрузка операций =======================
task('fraction', '26', 'Класс Fraction', 'hard', 'sem',
 '<p>Упражнение 12.2. Класс <code>Fraction</code>: приватные <code>numerator</code>, <code>denominator &gt; 0</code>, приватный <code>reduce()</code>, конструктор <code>Fraction(int num, int denom = 1)</code> сокращает дробь и делает знаменатель положительным, геттеры. Внешние операторы <code>+ - * /</code>, <code>== != &lt; &gt; &lt;= &gt;=</code> и <code>&lt;&lt;</code> в формате <code>3/4</code> (целые печатаются тоже как <code>n/1</code>).</p>',
 r'''#include <iostream>
#include <numeric>
class Fraction {
public:
    Fraction(int num, int denom = 1) : numerator(num), denominator(denom) { reduce(); }
    int getNumerator() const { return numerator; }
    int getDenominator() const { return denominator; }
private:
    int numerator, denominator;
    void reduce() {
        if (denominator < 0) { numerator = -numerator; denominator = -denominator; }
        int g = std::gcd(numerator, denominator);
        if (g > 1) { numerator /= g; denominator /= g; }
    }
};
Fraction operator+(const Fraction& a, const Fraction& b) { return Fraction(a.getNumerator() * b.getDenominator() + b.getNumerator() * a.getDenominator(), a.getDenominator() * b.getDenominator()); }
Fraction operator-(const Fraction& a, const Fraction& b) { return Fraction(a.getNumerator() * b.getDenominator() - b.getNumerator() * a.getDenominator(), a.getDenominator() * b.getDenominator()); }
Fraction operator*(const Fraction& a, const Fraction& b) { return Fraction(a.getNumerator() * b.getNumerator(), a.getDenominator() * b.getDenominator()); }
Fraction operator/(const Fraction& a, const Fraction& b) { return Fraction(a.getNumerator() * b.getDenominator(), a.getDenominator() * b.getNumerator()); }
bool operator==(const Fraction& a, const Fraction& b) { return a.getNumerator() == b.getNumerator() && a.getDenominator() == b.getDenominator(); }
bool operator!=(const Fraction& a, const Fraction& b) { return !(a == b); }
bool operator<(const Fraction& a, const Fraction& b) { return (long long)a.getNumerator() * b.getDenominator() < (long long)b.getNumerator() * a.getDenominator(); }
bool operator>(const Fraction& a, const Fraction& b) { return b < a; }
bool operator<=(const Fraction& a, const Fraction& b) { return !(b < a); }
bool operator>=(const Fraction& a, const Fraction& b) { return !(a < b); }
std::ostream& operator<<(std::ostream& os, const Fraction& f) { return os << f.getNumerator() << '/' << f.getDenominator(); }''',
 ['1 2 1 3', '2 -4 3 6', '0 5 7 1', '-3 4 5 -6'], mode='func',
 starter='#include <iostream>\n#include <numeric>\n\nclass Fraction {\npublic:\n    Fraction(int num, int denom = 1);\n    int getNumerator() const;\n    int getDenominator() const;\nprivate:\n    int numerator, denominator;\n    void reduce();\n};\n\n// внешние операторы + - * / == != < > <= >= <<\n',
 harness=r'''int main() {
    int a, b, c, d; std::cin >> a >> b >> c >> d;
    Fraction x(a, b), y(c, d);
    std::cout << x << ' ' << y << '\n';
    std::cout << x + y << ' ' << x - y << ' ' << x * y << ' ' << x / y << '\n';
    std::cout << (x == y) << (x != y) << (x < y) << (x > y) << (x <= y) << (x >= y) << '\n';
    std::cout << x + 1 << ' ' << (Fraction(2, 4) == Fraction(1, 2)) << '\n';
}''', inp='a b c d — дроби a/b и c/d (c ≠ 0).', out='Дроби, арифметика, сравнения.', hint='<code>std::gcd</code> из <code>&lt;numeric&gt;</code> работает и с отрицательными числами. <code>x + 1</code> компилируется благодаря неявному конструктору <code>Fraction(int)</code> — это и есть причина делать операторы внешними функциями.')

task('vec3', '26', 'Класс Vector3D', 'hard', 'sem',
 '<p>Упражнение 12.3 (сокращённо). <code>Vector3D</code> с конструкторами (по умолчанию — нулевой, с тремя параметрами), <code>double length() const</code>, <code>Vector3D normalized() const</code>, операторами <code>+</code>, <code>-</code> (унарный и бинарный), <code>* double</code> (с обеих сторон), <code>+=</code>, <code>[]</code> (две версии), <code>==</code> с точностью 1e-6, <code>&lt;&lt;</code> в формате <code>(1, 2, 3)</code>, <code>&gt;&gt;</code> и статическим <code>cross</code>.</p>',
 r'''#include <iostream>
#include <cmath>
class Vector3D {
public:
    Vector3D() : c_{0, 0, 0} {}
    Vector3D(double x, double y, double z) : c_{x, y, z} {}
    double length() const { return std::sqrt(c_[0] * c_[0] + c_[1] * c_[1] + c_[2] * c_[2]); }
    Vector3D normalized() const { double l = length(); return Vector3D(c_[0] / l, c_[1] / l, c_[2] / l); }
    double& operator[](int i) { return c_[i]; }
    const double& operator[](int i) const { return c_[i]; }
    Vector3D& operator+=(const Vector3D& o) { for (int i = 0; i < 3; ++i) c_[i] += o.c_[i]; return *this; }
    static Vector3D cross(const Vector3D& a, const Vector3D& b) {
        return Vector3D(a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]);
    }
private:
    double c_[3];
};
Vector3D operator+(Vector3D a, const Vector3D& b) { return a += b; }
Vector3D operator-(const Vector3D& a) { return Vector3D(-a[0], -a[1], -a[2]); }
Vector3D operator-(const Vector3D& a, const Vector3D& b) { return a + (-b); }
Vector3D operator*(const Vector3D& a, double k) { return Vector3D(a[0] * k, a[1] * k, a[2] * k); }
Vector3D operator*(double k, const Vector3D& a) { return a * k; }
bool operator==(const Vector3D& a, const Vector3D& b) {
    for (int i = 0; i < 3; ++i) if (std::fabs(a[i] - b[i]) > 1e-6) return false;
    return true;
}
bool operator!=(const Vector3D& a, const Vector3D& b) { return !(a == b); }
std::ostream& operator<<(std::ostream& os, const Vector3D& v) { return os << '(' << v[0] << ", " << v[1] << ", " << v[2] << ')'; }
std::istream& operator>>(std::istream& is, Vector3D& v) { return is >> v[0] >> v[1] >> v[2]; }''',
 ['1 0 0\n0 1 0', '3 4 0\n1 2 3', '1 1 1\n1 1 1'], mode='func',
 starter='#include <iostream>\n#include <cmath>\n\nclass Vector3D {\npublic:\n    // TODO\nprivate:\n    double c_[3];\n};\n',
 harness=r'''int main() {
    Vector3D a, b; std::cin >> a >> b;
    const Vector3D z;
    std::cout << a << ' ' << b << ' ' << z << '\n';
    std::cout << a + b << ' ' << a - b << ' ' << -a + z << '\n';
    std::cout << a * 2 << ' ' << 0.5 * b << '\n';
    std::cout << a.length() << ' ' << a.normalized() << ' ' << a.normalized().length() << '\n';
    std::cout << Vector3D::cross(a, b) << '\n';
    std::cout << (a == b) << (a != b) << (a + b - b == a) << ' ' << z[2] << '\n';
    a += b; a[0] = 7;
    std::cout << a << '\n';
}''', inp='Два вектора.', out='Результаты операций.', check='float')

task('matrixcls', '26', 'Класс Matrix', 'hard', 'sem',
 '<p>Упражнение 12.4 (сокращённо). <code>Matrix</code> хранит <code>double* data</code> одним блоком, размеры <code>rows_</code>, <code>cols_</code>; правило трёх; <code>Matrix(size_t r, size_t c)</code> заполняет нулями; <code>operator()(i, j)</code> в двух версиях; <code>transpose() const</code>; <code>+</code>, <code>*</code> на скаляр и матричное <code>*</code>; <code>&lt;&lt;</code> печатает каждую строку как <code>[1 2 3]</code>. Элемент (i, j) лежит в <code>data[i * cols_ + j]</code>.</p>',
 r'''#include <iostream>
#include <cstddef>
#include <utility>
class Matrix {
public:
    Matrix(size_t r, size_t c) : rows_(r), cols_(c), data(new double[r * c]{}) {}
    Matrix(const Matrix& o) : rows_(o.rows_), cols_(o.cols_), data(new double[o.rows_ * o.cols_]) {
        for (size_t i = 0; i < rows_ * cols_; ++i) data[i] = o.data[i];
    }
    Matrix& operator=(const Matrix& o) {
        if (this != &o) { Matrix t(o); std::swap(rows_, t.rows_); std::swap(cols_, t.cols_); std::swap(data, t.data); }
        return *this;
    }
    ~Matrix() { delete[] data; }
    size_t getRows() const { return rows_; }
    size_t getCols() const { return cols_; }
    double& operator()(size_t i, size_t j) { return data[i * cols_ + j]; }
    const double& operator()(size_t i, size_t j) const { return data[i * cols_ + j]; }
    Matrix transpose() const {
        Matrix t(cols_, rows_);
        for (size_t i = 0; i < rows_; ++i) for (size_t j = 0; j < cols_; ++j) t(j, i) = (*this)(i, j);
        return t;
    }
private:
    size_t rows_, cols_;
    double* data;
};
Matrix operator+(const Matrix& a, const Matrix& b) {
    Matrix r(a.getRows(), a.getCols());
    for (size_t i = 0; i < a.getRows(); ++i) for (size_t j = 0; j < a.getCols(); ++j) r(i, j) = a(i, j) + b(i, j);
    return r;
}
Matrix operator*(const Matrix& a, double k) {
    Matrix r(a.getRows(), a.getCols());
    for (size_t i = 0; i < a.getRows(); ++i) for (size_t j = 0; j < a.getCols(); ++j) r(i, j) = a(i, j) * k;
    return r;
}
Matrix operator*(const Matrix& a, const Matrix& b) {
    Matrix r(a.getRows(), b.getCols());
    for (size_t i = 0; i < a.getRows(); ++i)
        for (size_t j = 0; j < b.getCols(); ++j)
            for (size_t k = 0; k < a.getCols(); ++k) r(i, j) += a(i, k) * b(k, j);
    return r;
}
std::ostream& operator<<(std::ostream& os, const Matrix& m) {
    for (size_t i = 0; i < m.getRows(); ++i) {
        os << '[';
        for (size_t j = 0; j < m.getCols(); ++j) os << (j ? " " : "") << m(i, j);
        os << "]\n";
    }
    return os;
}''', ['2 3\n1 2 3\n4 5 6', '2 2\n1 2\n3 4', '1 1\n5'], mode='func',
 starter='#include <iostream>\n#include <cstddef>\n#include <utility>\n\nclass Matrix {\npublic:\n    Matrix(size_t rows, size_t cols);\n    // правило трёх, operator(), transpose, getRows/getCols\nprivate:\n    size_t rows_, cols_;\n    double* data;\n};\n\n// operator+, operator* (скаляр и матрица), operator<<\n',
 harness=r'''int main() {
    size_t r, c; std::cin >> r >> c;
    Matrix a(r, c);
    for (size_t i = 0; i < r; ++i) for (size_t j = 0; j < c; ++j) std::cin >> a(i, j);
    const Matrix t = a.transpose();
    std::cout << t << "--\n" << a + a << "--\n" << a * 0.5 << "--\n" << a * t << "--\n";
    Matrix b(1, 1);
    b = a; b(0, 0) = -1;
    std::cout << a(0, 0) << ' ' << b(0, 0) << ' ' << t(0, 0) << '\n';
}''', inp='r c и элементы.', out='Транспонированная, сумма, умножения, проверка копий.')
