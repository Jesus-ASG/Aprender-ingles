-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost
-- Tiempo de generación: 02-10-2022 a las 07:16:34
-- Versión del servidor: 10.4.24-MariaDB
-- Versión de PHP: 8.1.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `AprendeIngles`
--

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
('c0313fe3835beb55ac1afd75349e797888c10c90', '2022-09-14 02:40:52.920207', 1);

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
(44, 'Can view categorias', 11, 'view_categorias');

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
(1, 'pbkdf2_sha256$390000$EvDdO3VH3BWCxKll6NE0wo$7OImud9GVz3cnC6p9oY9MhMGQbWQEbKa8oR1vbK6Cek=', '2022-10-01 19:29:35.943537', 1, 'jesus', '', '', 'email@mail.com', 1, 1, '2022-08-26 13:55:37.342878'),
(15, 'pbkdf2_sha256$390000$FexWIh6YpNH08P3y72ZkdZ$ZlBXDFsaiQj7Z7vwDhTnVHhNmVae4NCFdog4f9sFiBw=', '2022-08-30 01:57:08.947420', 0, 'juanito', '', '', 'juanito1@email.com', 0, 1, '2022-08-30 01:57:08.436337'),
(16, 'pbkdf2_sha256$390000$ZIPx74AcRsMqW43079G9o6$4lOQHRSdFpvpbmeOWQZ1Elg1hTwyAk0qhqmKAie7Q74=', '2022-08-30 05:03:03.746542', 0, 'jbkj', '', '', 'mlml@m.com', 0, 1, '2022-08-30 05:03:03.225807'),
(17, 'pbkdf2_sha256$390000$oEs8gInVDhqmgNZkzZWsm0$PpGJZErm09tcTuwM2KB7DZcarTGTF5RqlG4VVJf8060=', '2022-08-31 14:07:31.008990', 0, 'sdasdas', '', '', 'sdasd@m.com', 0, 1, '2022-08-31 14:07:30.507223'),
(18, 'pbkdf2_sha256$390000$ScalzOpViCNkxq0wKWkEdv$Dz05/obDcvcc7p8tfjAA0a3IevQxB0m1m42h3lPqWPI=', '2022-09-05 23:10:49.209700', 0, 'jesus2', '', '', 'correo2@mail.com', 0, 1, '2022-09-05 23:10:48.654850'),
(19, 'pbkdf2_sha256$390000$0VM8JSJnF1ynC8mrRJlrrG$lJrgGeqtBkiM1igJqGRhKNFLzlZ3BwZhauk++pa/APU=', '2022-09-14 02:39:55.759340', 0, 'jesus3', '', '', 'jesus3@mail.com', 0, 1, '2022-09-13 23:24:58.116704');

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
(20, '2022-08-30 01:25:11.506051', '9', 'u', 3, '', 4, 1);

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
(11, 'main', 'categorias'),
(10, 'main', 'myuser'),
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
(27, 'main', '0002_categorias', '2022-10-02 04:23:17.930305');

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
('wvozcm7wltrx02boyqgvyuelqs9zgnfd', '.eJxVjEEOwiAQRe_C2hCGAVpcuvcMZMqAVA0kpV0Z765NutDtf-_9lwi0rSVsPS1hZnEWIE6_20TxkeoO-E711mRsdV3mSe6KPGiX18bpeTncv4NCvXxr1MY6rwGZQUMyxutshzRCRAKtCNBNAwCBM0pF50fMGFlnRus9pyzeH6TjNtI:1oeiB5:FiQs19VH9rIphzc9_dqtsr4dlP7keWsKyHkckyxmi9Y', '2022-10-15 19:29:35.947914');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `main_categorias`
--

CREATE TABLE `main_categorias` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `main_categorias`
--

INSERT INTO `main_categorias` (`id`, `nombre`) VALUES
(1, 'misterio'),
(2, 'comedia'),
(3, 'terror');

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
-- Indices de la tabla `main_categorias`
--
ALTER TABLE `main_categorias`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `main_user`
--
ALTER TABLE `main_user`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=45;

--
-- AUTO_INCREMENT de la tabla `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT de la tabla `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT de la tabla `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=28;

--
-- AUTO_INCREMENT de la tabla `main_categorias`
--
ALTER TABLE `main_categorias`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `main_user`
--
ALTER TABLE `main_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Restricciones para tablas volcadas
--

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
