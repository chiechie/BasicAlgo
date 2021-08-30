# 175. 组合两个表
# SQL架构
# 表1: Person

# +-------------+---------+
# | 列名         | 类型     |
# +-------------+---------+
# | PersonId    | int     |
# | FirstName   | varchar |
# | LastName    | varchar |
# +-------------+---------+
# PersonId 是上表主键
# 表2: Address

# +-------------+---------+
# | 列名         | 类型    |
# +-------------+---------+
# | AddressId   | int     |
# | PersonId    | int     |
# | City        | varchar |
# | State       | varchar |
# +-------------+---------+
# AddressId 是上表主键
 

# 编写一个 SQL 查询，满足条件：无论 person 是否有地址信息，都需要基于上述两表提供 person 的以下信息：
# FirstName, LastName, City, State
# https://leetcode-cn.com/problems/combine-two-tables/

# Write your MySQL query statement below
select a.FirstName, a.LastName, b.City, b.State
from Person as a left join Address as b
on a.PersonId = b.PersonId



-- 176. 第二高的薪水
-- SQL架构
-- 编写一个 SQL 查询，获取 Employee 表中第二高的薪水（Salary） 。

-- +----+--------+
-- | Id | Salary |
-- +----+--------+
-- | 1  | 100    |
-- | 2  | 200    |
-- | 3  | 300    |
-- +----+--------+
-- 例如上述 Employee 表，SQL查询应该返回 200 作为第二高的薪水。如果不存在第二高的薪水，那么查询应返回 null。

-- +---------------------+
-- | SecondHighestSalary |
-- +---------------------+
-- | 200                 |
-- +---------------------+
-- https://leetcode-cn.com/problems/second-highest-salary/solution/di-er-gao-de-xin-shui-by-leetcode/
# 方法1关键词: 嵌套，递归
select max(Salary) as SecondHighestSalary 
from Employee
where Salary < (select max(Salary) from Employee)

# 方法2关键词: offset, select 临时表 as 别名; 
select
(
select Salary as SecondHighestSalary 
from Employee
order by Salary desc
limit 1 offset 1) as SecondHighestSalary



-- 620. 有趣的电影
-- https://leetcode-cn.com/problems/not-boring-movies/
-- SQL架构
-- 某城市开了一家新的电影院，吸引了很多人过来看电影。该电影院特别注意用户体验，专门有个 LED显示板做电影推荐，上面公布着影评和相关电影描述。

-- 作为该电影院的信息部主管，您需要编写一个 SQL查询，找出所有影片描述为非 boring (不无聊) 的并且 id 为奇数 的影片，结果请按等级 rating 排列。

-- 例如，下表 cinema:

-- +---------+-----------+--------------+-----------+
-- |   id    | movie     |  description |  rating   |
-- +---------+-----------+--------------+-----------+
-- |   1     | War       |   great 3D   |   8.9     |
-- |   2     | Science   |   fiction    |   8.5     |
-- |   3     | irish     |   boring     |   6.2     |
-- |   4     | Ice song  |   Fantacy    |   8.6     |
-- |   5     | House card|   Interesting|   9.1     |
-- +---------+-----------+--------------+-----------+
-- 对于上面的例子，则正确的输出是为：

-- +---------+-----------+--------------+-----------+
-- |   id    | movie     |  description |  rating   |
-- +---------+-----------+--------------+-----------+
-- |   5     | House card|   Interesting|   9.1     |
-- |   1     | War       |   great 3D   |   8.9     |
-- +---------+-----------+--------------+-----------+

select * from cinema
where id % 2 = 1 and description != "boring"
order by rating desc

## 或者：求余 用 mod, where mod(id, 2) = 1 
select * from cinema
where  mod(id, 2) = 1  and description != "boring"
order by rating desc

-- 给定一个salary表，如下所示，有 m = 男性 和 f = 女性 的值。
-- 交换所有的 f 和 m 值（例如，将所有 f 值更改为 m，反之亦然）， 要求只使用一个更新（Update）语句，并且没有中间的临时表。

-- 注意，您必只能写一个 Update 语句，请不要编写任何 Select 语句。

-- 例如：

-- | id | name | sex | salary |
-- |----|------|-----|--------|
-- | 1  | A    | m   | 2500   |
-- | 2  | B    | f   | 1500   |
-- | 3  | C    | m   | 5500   |
-- | 4  | D    | f   | 500    |
-- 运行你所编写的更新语句之后，将会得到以下表:

-- | id | name | sex | salary |
-- |----|------|-----|--------|
-- | 1  | A    | f   | 2500   |
-- | 2  | B    | m   | 1500   |
-- | 3  | C    | f   | 5500   |
-- | 4  | D    | m   | 500    |

-- 来源：力扣（LeetCode）
-- 链接：https://leetcode-cn.com/problems/swap-salary

# 方法1的关键词: 使用 CASE...WHEN... 流程控制语句
UPDATE salary
SET sex = CASE sex  
	WHEN 'm' THEN 'f'
    ELSE 'm'
    END;

# 方法2的关键词：ascii和字母转换
update salary set sex = char(ascii('m') + ascii('f') - ascii(sex));





