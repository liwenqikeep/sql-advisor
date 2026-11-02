# 变量：无类型声明（但有类型注解，后面讲）
name: str = "zCloud"       # 对应 String name = "zCloud";
count = 0                  # 对应 int count = 0;

# 控制流：注意——没有大括号，用缩进；没有分号
if count > 0:
    print("positive")
elif count == 0:
    print("zero")
else:
    print("negative")

# 循环：for-in 遍历，没有传统 for(;;)
for i in range(3):         # range(3) = 0,1,2
    print(i)

# 函数：def 定义，无返回类型声明（可加注解）
def add(a: int, b: int = 0) -> int:   # b 有默认值，对标重载的替代方案
    return a + b



slow_sqls = ["SELECT * FROM t1", "SELECT * FROM t2"]
stats = {"db1": 120, "db2": 87}
stats.get("db3", 0)            # 对标 map.getOrDefault，没有 NPE 风险



nums = [1, 2, 3, 4, 5]

# Java: nums.stream().filter(n -> n % 2 == 0).map(n -> n * n).toList()
squares = [n * n for n in nums if n % 2 == 0]        # [4, 16]

# Java: map.entrySet().stream().collect(toMap(...))
doubled = {k: v * 2 for k, v in stats.items()}       # dict 推导式

# Java: list.stream().map(String::trim).toList()
cleaned = [s.strip() for s in slow_sqls]

# 带条件的「查存在」：Java anyMatch / allMatch
has_slow = any(len(s) > 15 for s in slow_sqls)       # 生成器表达式


def process(line):
    print(line)

def read_lines(path):
    with open(path, encoding="utf-8") as f:   # with = try-with-resources，自动关闭
        for line in f:
            yield line.strip()                 # yield：逐条产出，不占内存读全文件

for line in read_lines("slow_sql.log"):
    process(line)




# 类：Java 的简洁版，self 就是 this（必须显式写）
class LLMClient:
    def __init__(self, model: str, timeout: int = 30):   # __init__ = 构造函数
        self.model = model                                # self.xxx = 成员变量
        self.timeout = timeout

    def chat(self, prompt: str) -> str:
        return f"[{self.model}] {prompt}"

client = LLMClient(model="deepseek-chat")


# 异常：对标 try-catch-finally，语法更简洁
class ParseError(Exception):          # 自定义异常 = 继承 Exception
    pass

try:
    raise ParseError("bad sql")
except ParseError as e:               # as e = catch (ParseError e)
    print(f"解析失败: {e}")
finally:
    print("cleanup")



import time
from functools import wraps

def timed(fn):                         # 装饰器 = 一个「接收函数、返回函数」的函数
    @wraps(fn)
    def wrapper(*args, **kwargs):      # *args=可变参数, **kwargs=命名参数收集
        start = time.time()
        result = fn(*args, **kwargs)
        print(f"{fn.__name__} 耗时 {time.time() - start:.2f}s")
        return result
    return wrapper

@timed                                 # 对标 @Around AOP 切面
def slow_query():
    time.sleep(1)



from typing import Optional

def analyze(sql: str, params: list[str] | None = None) -> dict[str, float]:
    ...
# list[str]            对应 List<String>
# dict[str, float]     对应 Map<String, Double>
# str | None           对应 @Nullable String（3.10+ 语法）
# Optional[str]        等价于 str | None（老写法）