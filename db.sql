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

-- 177. 第N高的薪水
-- 编写一个 SQL 查询，获取 Employee 表中第 n 高的薪水（Salary）。

-- +----+--------+
-- | Id | Salary |
-- +----+--------+
-- | 1  | 100    |
-- | 2  | 200    |
-- | 3  | 300    |
-- +----+--------+
-- 例如上述 Employee 表，n = 2 时，应返回第二高的薪水 200。如果不存在第 n 高的薪水，那么查询应返回 null。

-- +------------------------+
-- | getNthHighestSalary(2) |
-- +------------------------+
-- | 200                    |
-- +------------------------+


CREATE FUNCTION getNthHighestSalary(N INT) RETURNS INT
BEGIN
set N:=N-1;
  RETURN (
      select Salary from Employee 
      GROUP BY  salary
      order by Salary desc 
      limit  N, 1
  );
END



--  178 分数排名
-- SQL架构
-- 编写一个 SQL 查询来实现分数排名。

-- 如果两个分数相同，则两个分数排名（Rank）相同。请注意，平分后的下一个名次应该是下一个连续的整数值。换句话说，名次之间不应该有“间隔”。

-- +----+-------+
-- | Id | Score |
-- +----+-------+
-- | 1  | 3.50  |
-- | 2  | 3.65  |
-- | 3  | 4.00  |
-- | 4  | 3.85  |
-- | 5  | 4.00  |
-- | 6  | 3.65  |
-- +----+-------+
-- 例如，根据上述给定的 Scores 表，你的查询应该返回（按分数从高到低排列）：

-- +-------+------+
-- | Score | Rank |
-- +-------+------+
-- | 4.00  | 1    |
-- | 4.00  | 1    |
-- | 3.85  | 2    |
-- | 3.65  | 3    |
-- | 3.65  | 3    |
-- | 3.50  | 4    |
-- +-------+------+
-- 重要提示：对于 MySQL 解决方案，如果要转义用作列名的保留字，可以在关键字之前和之后使用撇号。例如 `Rank`


select a.Score as Score,
(select count(distinct b.Score) from Scores b where b.Score >= a.Score) as  `Rank`
from Scores as a
order by a.Score DESC

select score, DENSE_RANK() OVER (ORDER BY Score DESC) as 'Rank' from Scores;


-- 181. 超过经理收入的员工
-- SQL架构
-- Employee 表包含所有员工，他们的经理也属于员工。每个员工都有一个 Id，此外还有一列对应员工的经理的 Id。

-- +----+-------+--------+-----------+
-- | Id | Name  | Salary | ManagerId |
-- +----+-------+--------+-----------+
-- | 1  | Joe   | 70000  | 3         |
-- | 2  | Henry | 80000  | 4         |
-- | 3  | Sam   | 60000  | NULL      |
-- | 4  | Max   | 90000  | NULL      |
-- +----+-------+--------+-----------+
-- 给定 Employee 表，编写一个 SQL 查询，该查询可以获取收入超过他们经理的员工的姓名。在上面的表格中，Joe 是唯一一个收入超过他的经理的员工。

-- +----------+
-- | Employee |
-- +----------+
-- | Joe      |
-- +----------+

# 关键词，select * from 表1，表2，是对表1和表2作笛卡尔积

select a.Name as Employee from Employee as a, Employee as b
where a.ManagerId = b.Id and a.Salary > b.Salary;


-- 182. 查找重复的电子邮箱
-- SQL架构
-- 编写一个 SQL 查询，查找 Person 表中所有重复的电子邮箱。

-- 示例：

-- +----+---------+
-- | Id | Email   |
-- +----+---------+
-- | 1  | a@b.com |
-- | 2  | c@d.com |
-- | 3  | a@b.com |
-- +----+---------+
-- 根据以上输入，你的查询应返回以下结果：

-- +---------+
-- | Email   |
-- +---------+
-- | a@b.com |
-- +---------+
-- 说明：所有电子邮箱都是小写字母。

# 关键词， select col1 from (select col1, col2 from t) as 临时表1 where cpl2 > 2
select Email from (
select Email, count(Email) as num from Person
GROUP by Email
) as statis
where num > 1;


-- 196. 删除重复的电子邮箱
-- SQL架构
-- 编写一个 SQL 查询，来删除 Person 表中所有重复的电子邮箱，重复的邮箱里只保留 Id 最小 的那个。

-- +----+------------------+
-- | Id | Email            |
-- +----+------------------+
-- | 1  | john@example.com |
-- | 2  | bob@example.com  |
-- | 3  | john@example.com |
-- +----+------------------+
-- Id 是这个表的主键。
-- 例如，在运行你的查询语句之后，上面的 Person 表应返回以下几行:

-- +----+------------------+
-- | Id | Email            |
-- +----+------------------+
-- | 1  | john@example.com |
-- | 2  | bob@example.com  |
-- +----+------------------+
 

-- 提示：
-- 执行 SQL 之后，输出是整个 Person 表。
-- 使用 delete 语句。

# delete 临时表1 from 临时表1， 临时表1 where *
# DELETE p1就表示从p1表中删除满足WHERE条件的记录。
# a. 从驱动表（左表）取出N条记录；
# b. 拿着这N条记录，依次到被驱动表（右表）查找满足WHERE条件的记录；
delete t1 from Person t1, Person t2
where t1.Email = t2.Email and t1.Id > t2.Id




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







