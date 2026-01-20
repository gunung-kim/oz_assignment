-- employees 테이블 생성
CREATE TABLE employees(
id INT AUTO_INCREMENT PRIMARY KEY,
name VARCHAR(100),
position VARCHAR(100),
salary DECIMAL(10,2)
);
-- 직원 데이터를 employees에 추가
INSERT INTO employees(name,`position`,salary)
VALUES ('혜린','PM',90000),
('은우','Frontend',80000),
('가을','Backend',92000),
('지수','Frontend',7800),
('민혁','Frontend',96000),
('하온','Backend',130000);
-- 모든 직원의 이름과 연봉 정보만 조회하는 쿼리
SELECT name,salary FROM employees;

-- Frontend직책을 가진 직원 중에서 연봉이 90000 이하인 직원의 이름과 연봉조회
SELECT name,salary FROM employees WHERE position='Frontend' AND salary <= 90000;
-- PM직책을 가진 모든 직원의 연봉을 10% 인상한 후 그결과를 확인
UPDATE employees SET salary = salary*0.1 + salary WHERE `position` = 'PM';
-- 모든 Backend 직책을 가지 직원의 연봉을 5%인상
UPDATE employees SET salary = salary*0.05 + salary WHERE `position` = 'Backend';
-- 민혁 사원의 데이터를 삭제
DELETE empolyees FROM empolyees WHERE name = '민혁'; 
-- 모든 직원을 position 별로 그룹화하여 각 직책의 평균연봉을 계산하세요
SELECT `position`,AVG(salary) AS avg_sal FROM employees GROUP BY `position`;
-- employees 테이블을 삭제하세요
DROP TABLE employees;
