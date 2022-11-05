-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 29-10-2022 a las 20:18:10
-- Versión del servidor: 10.4.24-MariaDB
-- Versión de PHP: 7.4.29

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `aprendeingles`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `app_categoria`
--

CREATE TABLE `app_categoria` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `app_categoria`
--

INSERT INTO `app_categoria` (`id`, `nombre`) VALUES
(1, 'Misterio'),
(2, 'Comedia'),
(3, 'Terror'),
(6, 'Cotidiano'),
(7, 'Computación'),
(8, 'Programación'),
(9, 'Redes'),
(10, 'Fútbol'),
(11, 'Otros'),
(12, 'Animales');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `app_historia`
--

CREATE TABLE `app_historia` (
  `id` int(11) NOT NULL,
  `titulo` varchar(100) NOT NULL,
  `portada` varchar(100) NOT NULL,
  `descripcion` varchar(100) DEFAULT NULL,
  `ruta` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `app_historia`
--

INSERT INTO `app_historia` (`id`, `titulo`, `portada`, `descripcion`, `ruta`) VALUES
(168, 'Historia de ejemplo', 'imagenes/portadas/book-default.png', 'Esta es una historia de ejemplo, cuenta con 4 categorías seleccionadas al azar y con 2 páginas.', 'historia-de-ejemplo'),
(169, 'Aprendiendo el abecedario', 'imagenes/portadas/imagen-abc-dl29456.webp', 'Abecedario', 'aprendiendo-el-abecedario'),
(170, 'Perrito', 'imagenes/portadas/descarga.jpg', 'No tiene páginas', 'perrito'),
(171, 'Gatitos', 'imagenes/portadas/purina-brand-que-saber-de-los-gatitos-bebes.webp', 'Gatitos en una foto', 'gatitos');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `app_historia_id_categoria`
--

CREATE TABLE `app_historia_id_categoria` (
  `id` bigint(20) NOT NULL,
  `historia_id` int(11) NOT NULL,
  `categoria_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `app_historia_id_categoria`
--

INSERT INTO `app_historia_id_categoria` (`id`, `historia_id`, `categoria_id`) VALUES
(129, 168, 1),
(130, 168, 3),
(131, 168, 6),
(132, 168, 7),
(133, 169, 1),
(134, 170, 11),
(135, 171, 11),
(136, 171, 12);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `app_historia_pagina`
--

CREATE TABLE `app_historia_pagina` (
  `id` int(11) NOT NULL,
  `texto` varchar(800) NOT NULL,
  `historia_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `app_historia_pagina`
--

INSERT INTO `app_historia_pagina` (`id`, `texto`, `historia_id`) VALUES
(59, 'Página 1 de la historia de ejemplo', 168),
(60, 'Página 2 de la historia de ejemplo', 168),
(61, 'A', 169),
(62, 'B', 169),
(63, 'C', 169),
(64, 'D', 169),
(65, 'E\r\nF\r\nG\r\nH\r\nI', 169),
(66, 'Página 1', 171),
(67, 'Página 2', 171);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `app_pag_conversation`
--

CREATE TABLE `app_pag_conversation` (
  `id` int(11) NOT NULL,
  `name` varchar(30) NOT NULL,
  `content` varchar(255) NOT NULL,
  `translation` varchar(255) NOT NULL,
  `page_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `app_pag_question`
--

CREATE TABLE `app_pag_question` (
  `id` int(11) NOT NULL,
  `question` varchar(255) NOT NULL,
  `page_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `app_pag_question_option`
--

CREATE TABLE `app_pag_question_option` (
  `id` int(11) NOT NULL,
  `answer` varchar(255) NOT NULL,
  `correct` tinyint(1) NOT NULL,
  `question_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `app_pag_repeat_phrase`
--

CREATE TABLE `app_pag_repeat_phrase` (
  `id` int(11) NOT NULL,
  `content` varchar(255) NOT NULL,
  `translation` varchar(255) NOT NULL,
  `page_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `authtoken_token`
--

CREATE TABLE `authtoken_token` (
  `key` varchar(40) NOT NULL,
  `created` datetime(6) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `authtoken_token`
--

INSERT INTO `authtoken_token` (`key`, `created`, `user_id`) VALUES
('dda73440351d6c798b80294a0bbc080b05b94230', '2022-10-27 04:30:06.304912', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add user', 4, 'add_user'),
(14, 'Can change user', 4, 'change_user'),
(15, 'Can delete user', 4, 'delete_user'),
(16, 'Can view user', 4, 'view_user'),
(17, 'Can add content type', 5, 'add_contenttype'),
(18, 'Can change content type', 5, 'change_contenttype'),
(19, 'Can delete content type', 5, 'delete_contenttype'),
(20, 'Can view content type', 5, 'view_contenttype'),
(21, 'Can add session', 6, 'add_session'),
(22, 'Can change session', 6, 'change_session'),
(23, 'Can delete session', 6, 'delete_session'),
(24, 'Can view session', 6, 'view_session'),
(25, 'Can add user', 7, 'add_user'),
(26, 'Can change user', 7, 'change_user'),
(27, 'Can delete user', 7, 'delete_user'),
(28, 'Can view user', 7, 'view_user'),
(29, 'Can add Token', 8, 'add_token'),
(30, 'Can change Token', 8, 'change_token'),
(31, 'Can delete Token', 8, 'delete_token'),
(32, 'Can view Token', 8, 'view_token'),
(33, 'Can add token', 9, 'add_tokenproxy'),
(34, 'Can change token', 9, 'change_tokenproxy'),
(35, 'Can delete token', 9, 'delete_tokenproxy'),
(36, 'Can view token', 9, 'view_tokenproxy'),
(37, 'Can add my user', 10, 'add_myuser'),
(38, 'Can change my user', 10, 'change_myuser'),
(39, 'Can delete my user', 10, 'delete_myuser'),
(40, 'Can view my user', 10, 'view_myuser'),
(41, 'Can add categorias', 11, 'add_categorias'),
(42, 'Can change categorias', 11, 'change_categorias'),
(43, 'Can delete categorias', 11, 'delete_categorias'),
(44, 'Can view categorias', 11, 'view_categorias'),
(45, 'Can add historia', 12, 'add_historia'),
(46, 'Can change historia', 12, 'change_historia'),
(47, 'Can delete historia', 12, 'delete_historia'),
(48, 'Can view historia', 12, 'view_historia'),
(49, 'Can add categoria', 11, 'add_categoria'),
(50, 'Can change categoria', 11, 'change_categoria'),
(51, 'Can delete categoria', 11, 'delete_categoria'),
(52, 'Can view categoria', 11, 'view_categoria'),
(53, 'Can add pagina', 13, 'add_pagina'),
(54, 'Can change pagina', 13, 'change_pagina'),
(55, 'Can delete pagina', 13, 'delete_pagina'),
(56, 'Can view pagina', 13, 'view_pagina'),
(57, 'Can add repeat phrase', 14, 'add_repeatphrase'),
(58, 'Can change repeat phrase', 14, 'change_repeatphrase'),
(59, 'Can delete repeat phrase', 14, 'delete_repeatphrase'),
(60, 'Can view repeat phrase', 14, 'view_repeatphrase'),
(61, 'Can add question', 15, 'add_question'),
(62, 'Can change question', 15, 'change_question'),
(63, 'Can delete question', 15, 'delete_question'),
(64, 'Can view question', 15, 'view_question'),
(65, 'Can add option', 16, 'add_option'),
(66, 'Can change option', 16, 'change_option'),
(67, 'Can delete option', 16, 'delete_option'),
(68, 'Can view option', 16, 'view_option'),
(69, 'Can add dialogue', 17, 'add_dialogue'),
(70, 'Can change dialogue', 17, 'change_dialogue'),
(71, 'Can delete dialogue', 17, 'delete_dialogue'),
(72, 'Can view dialogue', 17, 'view_dialogue');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user`
--

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `auth_user`
--

INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
(1, 'pbkdf2_sha256$390000$EvDdO3VH3BWCxKll6NE0wo$7OImud9GVz3cnC6p9oY9MhMGQbWQEbKa8oR1vbK6Cek=', '2022-10-29 18:12:24.220623', 1, 'jesus', '', '', 'email@mail.com', 1, 1, '2022-08-26 13:55:37.342878'),
(20, 'pbkdf2_sha256$390000$NaVJMsErLrDNUcg4xc2xJ5$3l/jJrHv05k0J9WfM1wtR0bQR1UTdWnor6vxi8Njpq8=', '2022-10-24 06:16:06.219619', 0, 'usuario', '', '', 'usuario@correo.com', 0, 1, '2022-10-22 19:45:06.208655');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user_groups`
--

CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user_user_permissions`
--

CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `django_admin_log`
--

INSERT INTO `django_admin_log` (`id`, `action_time`, `object_id`, `object_repr`, `action_flag`, `change_message`, `content_type_id`, `user_id`) VALUES
(1, '2022-08-26 13:57:23.417297', '1', 'id: 1\nusername: jesus\npassword: 123', 1, '[{\"added\": {}}]', 7, 1),
(2, '2022-08-26 13:57:41.804319', '2', 'id: 2\nusername: user\npassword: 123', 1, '[{\"added\": {}}]', 7, 1),
(3, '2022-08-27 17:55:44.722266', '1', 'da4a0373057028e2f0cc5f248b20dc73317362a5', 3, '', 9, 1),
(4, '2022-08-27 18:49:35.391025', '1', 'b03e7219fed8491c6b17887f6ad9fd4cb68c3d6d', 3, '', 9, 1),
(5, '2022-08-28 00:51:42.010053', '1', '25d3a2e2704e9411c3d34e94074f39d1c807d94c', 3, '', 9, 1),
(7, '2022-08-29 16:02:15.753635', '2', '2cb0a604e8e1c1438f0f7ae434a2aaaf3eec8e3b', 3, '', 9, 1),
(8, '2022-08-29 20:04:46.485319', '4', 'authnew', 3, '', 4, 1),
(9, '2022-08-29 20:04:46.487841', '3', 'hola', 3, '', 4, 1),
(10, '2022-08-29 20:04:46.489289', '6', 'kmkkmk', 3, '', 4, 1),
(11, '2022-08-29 20:04:46.491545', '5', 'lklklkl', 3, '', 4, 1),
(12, '2022-08-29 20:04:46.492956', '7', 'lmlm', 3, '', 4, 1),
(13, '2022-08-29 20:04:46.494626', '8', 'sada', 3, '', 4, 1),
(14, '2022-08-29 20:04:46.495842', '2', 'user', 3, '', 4, 1),
(15, '2022-08-30 01:25:11.495038', '11', 'a', 3, '', 4, 1),
(16, '2022-08-30 01:25:11.497389', '10', 'aaa', 3, '', 4, 1),
(17, '2022-08-30 01:25:11.500545', '13', 'dfaf', 3, '', 4, 1),
(18, '2022-08-30 01:25:11.501808', '12', 'kkn', 3, '', 4, 1),
(19, '2022-08-30 01:25:11.504515', '14', 'kljhjvb', 3, '', 4, 1),
(20, '2022-08-30 01:25:11.506051', '9', 'u', 3, '', 4, 1),
(21, '2022-10-06 12:54:19.516168', '3', '3 mkmkm', 2, '[{\"changed\": {\"fields\": [\"Id categoria\"]}}]', 12, 1),
(22, '2022-10-06 13:13:44.094234', '3', '3 Historia 2', 2, '[{\"changed\": {\"fields\": [\"Titulo\", \"Descripcion\"]}}]', 12, 1),
(23, '2022-10-06 13:15:32.519675', '4', '4 Historia nueva', 1, '[{\"added\": {}}]', 12, 1),
(24, '2022-10-06 21:50:00.912960', '8', '8 desc1', 2, '[{\"changed\": {\"fields\": [\"Id categoria\"]}}]', 12, 1),
(25, '2022-10-07 23:21:51.168694', '14', '14 hist', 1, '[{\"added\": {}}]', 12, 1),
(26, '2022-10-08 00:07:18.051907', '16', '16 h1', 1, '[{\"added\": {}}]', 12, 1),
(27, '2022-10-08 00:07:39.638943', '17', '17 h2', 1, '[{\"added\": {}}]', 12, 1),
(28, '2022-10-08 00:44:24.825096', '22', '22 l54', 1, '[{\"added\": {}}]', 12, 1),
(29, '2022-10-08 01:41:29.298926', '26', '26 m', 2, '[{\"changed\": {\"fields\": [\"Id categoria\"]}}]', 12, 1),
(30, '2022-10-14 02:43:17.947165', '1', 'Pagina object (1)', 1, '[{\"added\": {}}]', 13, 1),
(31, '2022-10-14 02:43:25.506363', '2', 'Pagina object (2)', 1, '[{\"added\": {}}]', 13, 1),
(32, '2022-10-14 02:43:45.100029', '8', '8 desc1', 2, '[{\"changed\": {\"fields\": [\"Pagina\"]}}]', 12, 1),
(33, '2022-10-14 02:43:58.702567', '28', '28 Historia prueba 1', 2, '[{\"changed\": {\"fields\": [\"Pagina\"]}}]', 12, 1),
(34, '2022-10-14 02:50:44.338262', '2', 'Pagina object (2)', 2, '[{\"changed\": {\"fields\": [\"Historia\"]}}]', 13, 1),
(35, '2022-10-14 02:51:04.667004', '1', 'Pagina object (1)', 2, '[{\"changed\": {\"fields\": [\"Historia\"]}}]', 13, 1),
(36, '2022-10-23 19:02:14.441953', '138', 'q w  www', 2, '[{\"changed\": {\"fields\": [\"Id categoria\"]}}]', 12, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'auth', 'user'),
(8, 'authtoken', 'token'),
(9, 'authtoken', 'tokenproxy'),
(5, 'contenttypes', 'contenttype'),
(11, 'main', 'categoria'),
(17, 'main', 'dialogue'),
(12, 'main', 'historia'),
(10, 'main', 'myuser'),
(16, 'main', 'option'),
(13, 'main', 'pagina'),
(15, 'main', 'question'),
(14, 'main', 'repeatphrase'),
(7, 'main', 'user'),
(6, 'sessions', 'session');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2022-08-26 13:46:44.798415'),
(2, 'auth', '0001_initial', '2022-08-26 13:46:44.957127'),
(3, 'admin', '0001_initial', '2022-08-26 13:46:45.000664'),
(4, 'admin', '0002_logentry_remove_auto_add', '2022-08-26 13:46:45.010499'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2022-08-26 13:46:45.020263'),
(6, 'contenttypes', '0002_remove_content_type_name', '2022-08-26 13:46:45.050880'),
(7, 'auth', '0002_alter_permission_name_max_length', '2022-08-26 13:46:45.071298'),
(8, 'auth', '0003_alter_user_email_max_length', '2022-08-26 13:46:45.083010'),
(9, 'auth', '0004_alter_user_username_opts', '2022-08-26 13:46:45.091480'),
(10, 'auth', '0005_alter_user_last_login_null', '2022-08-26 13:46:45.108377'),
(11, 'auth', '0006_require_contenttypes_0002', '2022-08-26 13:46:45.110763'),
(12, 'auth', '0007_alter_validators_add_error_messages', '2022-08-26 13:46:45.122323'),
(13, 'auth', '0008_alter_user_username_max_length', '2022-08-26 13:46:45.131907'),
(14, 'auth', '0009_alter_user_last_name_max_length', '2022-08-26 13:46:45.144947'),
(15, 'auth', '0010_alter_group_name_max_length', '2022-08-26 13:46:45.154842'),
(16, 'auth', '0011_update_proxy_permissions', '2022-08-26 13:46:45.162137'),
(17, 'auth', '0012_alter_user_first_name_max_length', '2022-08-26 13:46:45.172432'),
(18, 'main', '0001_initial', '2022-08-26 13:46:45.180134'),
(19, 'sessions', '0001_initial', '2022-08-26 13:46:45.198525'),
(20, 'authtoken', '0001_initial', '2022-08-26 17:00:28.424987'),
(21, 'authtoken', '0002_auto_20160226_1747', '2022-08-26 17:00:28.461583'),
(22, 'authtoken', '0003_tokenproxy', '2022-08-26 17:00:28.466092'),
(23, 'main', '0002_myuser', '2022-08-28 16:10:31.619576'),
(24, 'main', '0003_alter_myuser_email', '2022-08-28 16:10:31.625997'),
(25, 'main', '0004_delete_user', '2022-08-28 16:10:31.633226'),
(26, 'main', '0005_user_delete_myuser', '2022-08-28 16:10:31.649172'),
(27, 'main', '0002_categorias', '2022-10-02 04:23:17.930305'),
(28, 'main', '0003_historia_rename_categorias_categoria', '2022-10-06 04:41:11.223810'),
(29, 'main', '0004_categoriadehistoria', '2022-10-06 04:41:11.232860'),
(30, 'main', '0005_alter_categoriadehistoria_id_categoria_and_more', '2022-10-06 04:41:11.239259'),
(31, 'main', '0006_alter_historia_descripcion_alter_historia_portada', '2022-10-06 04:41:11.261538'),
(32, 'main', '0007_delete_categoriadehistoria_historia_id_categoria', '2022-10-06 04:41:11.314552'),
(33, 'main', '0008_alter_historia_id_categoria', '2022-10-06 13:18:13.500125'),
(34, 'main', '0009_alter_historia_id_categoria', '2022-10-06 13:18:55.369804'),
(35, 'main', '0010_alter_historia_portada', '2022-10-06 14:32:26.224368'),
(36, 'main', '0011_alter_historia_descripcion_and_more', '2022-10-08 02:38:13.752716'),
(37, 'main', '0012_pagina', '2022-10-14 02:08:05.630944'),
(38, 'main', '0013_historia_pagina', '2022-10-14 02:40:01.351827'),
(39, 'main', '0014_remove_historia_pagina_pagina_historia', '2022-10-14 02:49:58.011773'),
(40, 'main', '0015_alter_pagina_texto', '2022-10-16 17:34:00.698001'),
(41, 'main', '0016_historia_ruta', '2022-10-23 20:10:18.874148'),
(42, 'main', '0017_alter_historia_ruta', '2022-10-23 20:22:05.956615'),
(43, 'main', '0018_alter_pagina_id', '2022-10-29 18:13:26.789585'),
(44, 'main', '0019_alter_categoria_table_alter_historia_table_and_more', '2022-10-29 18:13:27.173320');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('0mmb6npv0gm5v7zazz4x6n3bjwdtb4w0', '.eJxVjEEOwiAQRe_C2hCGAVpcuvcMZMqAVA0kpV0Z765NutDtf-_9lwi0rSVsPS1hZnEWIE6_20TxkeoO-E711mRsdV3mSe6KPGiX18bpeTncv4NCvXxr1MY6rwGZQUMyxutshzRCRAKtCNBNAwCBM0pF50fMGFlnRus9pyzeH6TjNtI:1oYIKa:b9yCCmj1AJBECmBcDchNkk1DCzgjqg6nEPbARFw33Uc', '2022-09-28 02:40:52.932086'),
('ghat0eump2a416z40ovj7ua3l8jhjuuw', '.eJxVjEEOwiAQRe_C2hCGAVpcuvcMZMqAVA0kpV0Z765NutDtf-_9lwi0rSVsPS1hZnEWIE6_20TxkeoO-E711mRsdV3mSe6KPGiX18bpeTncv4NCvXxr1MY6rwGZQUMyxutshzRCRAKtCNBNAwCBM0pF50fMGFlnRus9pyzeH6TjNtI:1omKMU:sMN9WKhXS6P2Luh1YZxoKk0LTXRDlUpr9222V4ca-Y4', '2022-11-05 19:40:50.792637'),
('hafbq7zchrpnqvq2dlw400g49p8f614e', '.eJxVjEEOwiAQRe_C2hCGAVpcuvcMZMqAVA0kpV0Z765NutDtf-_9lwi0rSVsPS1hZnEWIE6_20TxkeoO-E711mRsdV3mSe6KPGiX18bpeTncv4NCvXxr1MY6rwGZQUMyxutshzRCRAKtCNBNAwCBM0pF50fMGFlnRus9pyzeH6TjNtI:1omKO8:PVHEVEbQBbILIG-xL3CD8yAV8MSuOsTt7Zo_iB1B3H8', '2022-11-05 19:42:32.237781'),
('n6k5dxpev32a0qxurt5q7qi7ry8cxtev', '.eJxVjEEOwiAQRe_C2hCGAVpcuvcMZMqAVA0kpV0Z765NutDtf-_9lwi0rSVsPS1hZnEWIE6_20TxkeoO-E711mRsdV3mSe6KPGiX18bpeTncv4NCvXxr1MY6rwGZQUMyxutshzRCRAKtCNBNAwCBM0pF50fMGFlnRus9pyzeH6TjNtI:1onuWs:PZhbb1acr3OCewsO5OuHDHnjtBc7m9-KoJbDDh5yEeA', '2022-11-10 04:30:06.320833'),
('qynqh05v8uijtp6imfr511199fsnqmaa', '.eJxVjEEOwiAQRe_C2hCGAVpcuvcMZMqAVA0kpV0Z765NutDtf-_9lwi0rSVsPS1hZnEWIE6_20TxkeoO-E711mRsdV3mSe6KPGiX18bpeTncv4NCvXxr1MY6rwGZQUMyxutshzRCRAKtCNBNAwCBM0pF50fMGFlnRus9pyzeH6TjNtI:1omKN2:dBh_t5rcxfjRHiQ4F-BaLoT7aKf6Ozbo5EBwZWeSn_Q', '2022-11-05 19:41:24.080897'),
('wvozcm7wltrx02boyqgvyuelqs9zgnfd', '.eJxVjEEOwiAQRe_C2hCGAVpcuvcMZMqAVA0kpV0Z765NutDtf-_9lwi0rSVsPS1hZnEWIE6_20TxkeoO-E711mRsdV3mSe6KPGiX18bpeTncv4NCvXxr1MY6rwGZQUMyxutshzRCRAKtCNBNAwCBM0pF50fMGFlnRus9pyzeH6TjNtI:1oeiB5:FiQs19VH9rIphzc9_dqtsr4dlP7keWsKyHkckyxmi9Y', '2022-10-15 19:29:35.947914'),
('zpnjfo0pahdrl34kwh8nyqddr7ahyszh', '.eJxVjEEOwiAQRe_C2hCGAVpcuvcMZMqAVA0kpV0Z765NutDtf-_9lwi0rSVsPS1hZnEWIE6_20TxkeoO-E711mRsdV3mSe6KPGiX18bpeTncv4NCvXxr1MY6rwGZQUMyxutshzRCRAKtCNBNAwCBM0pF50fMGFlnRus9pyzeH6TjNtI:1ooqJk:deP2NOL_GX9a9Cy3X02L63QukPT1gIEwe5HsV3w41r8', '2022-11-12 18:12:24.224083');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `main_user`
--

CREATE TABLE `main_user` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `main_user`
--

INSERT INTO `main_user` (`id`, `username`, `password`) VALUES
(1, 'hhh', '123');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `app_categoria`
--
ALTER TABLE `app_categoria`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `app_historia`
--
ALTER TABLE `app_historia`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `app_historia_id_categoria`
--
ALTER TABLE `app_historia_id_categoria`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `main_historia_id_categor_historia_id_categoria_id_4ae0f7bc_uniq` (`historia_id`,`categoria_id`),
  ADD KEY `main_historia_id_cat_categoria_id_38ef862e_fk_main_cate` (`categoria_id`);

--
-- Indices de la tabla `app_historia_pagina`
--
ALTER TABLE `app_historia_pagina`
  ADD PRIMARY KEY (`id`),
  ADD KEY `main_pagina_historia_id_e74b548d_fk_main_historia_id` (`historia_id`);

--
-- Indices de la tabla `app_pag_conversation`
--
ALTER TABLE `app_pag_conversation`
  ADD PRIMARY KEY (`id`),
  ADD KEY `app_pag_conversation_page_id_98039c29_fk_app_historia_pagina_id` (`page_id`);

--
-- Indices de la tabla `app_pag_question`
--
ALTER TABLE `app_pag_question`
  ADD PRIMARY KEY (`id`),
  ADD KEY `app_pag_question_page_id_78625dd5_fk_app_historia_pagina_id` (`page_id`);

--
-- Indices de la tabla `app_pag_question_option`
--
ALTER TABLE `app_pag_question_option`
  ADD PRIMARY KEY (`id`),
  ADD KEY `app_pag_question_opt_question_id_680ccdd2_fk_app_pag_q` (`question_id`);

--
-- Indices de la tabla `app_pag_repeat_phrase`
--
ALTER TABLE `app_pag_repeat_phrase`
  ADD PRIMARY KEY (`id`),
  ADD KEY `app_pag_repeat_phrase_page_id_cecba90a_fk_app_historia_pagina_id` (`page_id`);

--
-- Indices de la tabla `authtoken_token`
--
ALTER TABLE `authtoken_token`
  ADD PRIMARY KEY (`key`),
  ADD UNIQUE KEY `user_id` (`user_id`);

--
-- Indices de la tabla `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indices de la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indices de la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indices de la tabla `auth_user`
--
ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indices de la tabla `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  ADD KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`);

--
-- Indices de la tabla `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  ADD KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`);

--
-- Indices de la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`);

--
-- Indices de la tabla `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indices de la tabla `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Indices de la tabla `main_user`
--
ALTER TABLE `main_user`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `app_categoria`
--
ALTER TABLE `app_categoria`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT de la tabla `app_historia`
--
ALTER TABLE `app_historia`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=172;

--
-- AUTO_INCREMENT de la tabla `app_historia_id_categoria`
--
ALTER TABLE `app_historia_id_categoria`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=137;

--
-- AUTO_INCREMENT de la tabla `app_historia_pagina`
--
ALTER TABLE `app_historia_pagina`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=68;

--
-- AUTO_INCREMENT de la tabla `app_pag_conversation`
--
ALTER TABLE `app_pag_conversation`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `app_pag_question`
--
ALTER TABLE `app_pag_question`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `app_pag_question_option`
--
ALTER TABLE `app_pag_question_option`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `app_pag_repeat_phrase`
--
ALTER TABLE `app_pag_repeat_phrase`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=73;

--
-- AUTO_INCREMENT de la tabla `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT de la tabla `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=37;

--
-- AUTO_INCREMENT de la tabla `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT de la tabla `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=45;

--
-- AUTO_INCREMENT de la tabla `main_user`
--
ALTER TABLE `main_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `app_historia_id_categoria`
--
ALTER TABLE `app_historia_id_categoria`
  ADD CONSTRAINT `main_historia_id_cat_categoria_id_38ef862e_fk_main_cate` FOREIGN KEY (`categoria_id`) REFERENCES `app_categoria` (`id`),
  ADD CONSTRAINT `main_historia_id_cat_historia_id_2fc7a487_fk_main_hist` FOREIGN KEY (`historia_id`) REFERENCES `app_historia` (`id`);

--
-- Filtros para la tabla `app_historia_pagina`
--
ALTER TABLE `app_historia_pagina`
  ADD CONSTRAINT `main_pagina_historia_id_e74b548d_fk_main_historia_id` FOREIGN KEY (`historia_id`) REFERENCES `app_historia` (`id`);

--
-- Filtros para la tabla `app_pag_conversation`
--
ALTER TABLE `app_pag_conversation`
  ADD CONSTRAINT `app_pag_conversation_page_id_98039c29_fk_app_historia_pagina_id` FOREIGN KEY (`page_id`) REFERENCES `app_historia_pagina` (`id`);

--
-- Filtros para la tabla `app_pag_question`
--
ALTER TABLE `app_pag_question`
  ADD CONSTRAINT `app_pag_question_page_id_78625dd5_fk_app_historia_pagina_id` FOREIGN KEY (`page_id`) REFERENCES `app_historia_pagina` (`id`);

--
-- Filtros para la tabla `app_pag_question_option`
--
ALTER TABLE `app_pag_question_option`
  ADD CONSTRAINT `app_pag_question_opt_question_id_680ccdd2_fk_app_pag_q` FOREIGN KEY (`question_id`) REFERENCES `app_pag_question` (`id`);

--
-- Filtros para la tabla `app_pag_repeat_phrase`
--
ALTER TABLE `app_pag_repeat_phrase`
  ADD CONSTRAINT `app_pag_repeat_phrase_page_id_cecba90a_fk_app_historia_pagina_id` FOREIGN KEY (`page_id`) REFERENCES `app_historia_pagina` (`id`);

--
-- Filtros para la tabla `authtoken_token`
--
ALTER TABLE `authtoken_token`
  ADD CONSTRAINT `authtoken_token_user_id_35299eff_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Filtros para la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Filtros para la tabla `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
