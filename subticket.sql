-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- 主机： localhost
-- 生成日期： 2025-02-24 13:21:43
-- 服务器版本： 8.0.37
-- PHP 版本： 8.2.23

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 数据库： `subticket`
--

-- --------------------------------------------------------

--
-- 表的结构 `groups`
--

CREATE TABLE `groups` (
  `id` int NOT NULL,
  `group_name` varchar(1000) COLLATE utf8mb4_general_ci NOT NULL,
  `group_id` varchar(64) COLLATE utf8mb4_general_ci NOT NULL,
  `users` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- 表的结构 `links`
--

CREATE TABLE `links` (
  `id` int NOT NULL,
  `link` tinytext COLLATE utf8mb4_general_ci NOT NULL,
  `source` bigint NOT NULL,
  `dest` bigint NOT NULL,
  `exp` datetime NOT NULL,
  `requests` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- 表的结构 `log`
--

CREATE TABLE `log` (
  `id` int NOT NULL,
  `time` datetime NOT NULL,
  `new_id` bigint NOT NULL,
  `old_id` bigint NOT NULL,
  `group_id` bigint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- 表的结构 `tickets`
--

CREATE TABLE `tickets` (
  `id` int NOT NULL,
  `user_id` bigint NOT NULL,
  `user_name` char(64) COLLATE utf8mb4_general_ci NOT NULL,
  `nickname` char(64) COLLATE utf8mb4_general_ci NOT NULL,
  `ticket_key` char(128) COLLATE utf8mb4_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 转储表的索引
--

--
-- 表的索引 `groups`
--
ALTER TABLE `groups`
  ADD PRIMARY KEY (`id`);

--
-- 表的索引 `links`
--
ALTER TABLE `links`
  ADD PRIMARY KEY (`id`);

--
-- 表的索引 `log`
--
ALTER TABLE `log`
  ADD PRIMARY KEY (`id`);

--
-- 表的索引 `tickets`
--
ALTER TABLE `tickets`
  ADD PRIMARY KEY (`id`);

--
-- 在导出的表使用AUTO_INCREMENT
--

--
-- 使用表AUTO_INCREMENT `groups`
--
ALTER TABLE `groups`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- 使用表AUTO_INCREMENT `links`
--
ALTER TABLE `links`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- 使用表AUTO_INCREMENT `log`
--
ALTER TABLE `log`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- 使用表AUTO_INCREMENT `tickets`
--
ALTER TABLE `tickets`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
