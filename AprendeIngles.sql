-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 08-11-2022 a las 05:02:58
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
('2a04d8fa5e172f9b672450d841d8c739760c8e71', '2022-11-08 04:02:42.385389', 1);

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
(25, 'Can add Token', 7, 'add_token'),
(26, 'Can change Token', 7, 'change_token'),
(27, 'Can delete Token', 7, 'delete_token'),
(28, 'Can view Token', 7, 'view_token'),
(29, 'Can add token', 8, 'add_tokenproxy'),
(30, 'Can change token', 8, 'change_tokenproxy'),
(31, 'Can delete token', 8, 'delete_tokenproxy'),
(32, 'Can view token', 8, 'view_tokenproxy'),
(33, 'Can add page', 9, 'add_page'),
(34, 'Can change page', 9, 'change_page'),
(35, 'Can delete page', 9, 'delete_page'),
(36, 'Can view page', 9, 'view_page'),
(37, 'Can add tag', 10, 'add_tag'),
(38, 'Can change tag', 10, 'change_tag'),
(39, 'Can delete tag', 10, 'delete_tag'),
(40, 'Can view tag', 10, 'view_tag'),
(41, 'Can add user', 11, 'add_user'),
(42, 'Can change user', 11, 'change_user'),
(43, 'Can delete user', 11, 'delete_user'),
(44, 'Can view user', 11, 'view_user'),
(45, 'Can add story', 12, 'add_story'),
(46, 'Can change story', 12, 'change_story'),
(47, 'Can delete story', 12, 'delete_story'),
(48, 'Can view story', 12, 'view_story'),
(49, 'Can add repeat phrase', 13, 'add_repeatphrase'),
(50, 'Can change repeat phrase', 13, 'change_repeatphrase'),
(51, 'Can delete repeat phrase', 13, 'delete_repeatphrase'),
(52, 'Can view repeat phrase', 13, 'view_repeatphrase'),
(53, 'Can add question', 14, 'add_question'),
(54, 'Can change question', 14, 'change_question'),
(55, 'Can delete question', 14, 'delete_question'),
(56, 'Can view question', 14, 'view_question'),
(57, 'Can add option', 15, 'add_option'),
(58, 'Can change option', 15, 'change_option'),
(59, 'Can delete option', 15, 'delete_option'),
(60, 'Can view option', 15, 'view_option'),
(61, 'Can add dialogue', 16, 'add_dialogue'),
(62, 'Can change dialogue', 16, 'change_dialogue'),
(63, 'Can delete dialogue', 16, 'delete_dialogue'),
(64, 'Can view dialogue', 16, 'view_dialogue');

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
(1, 'pbkdf2_sha256$390000$XtXhoZzPl1fCjaEX2Xgnju$WWdPmQ0Srb+PGLbwwNPzMdM7ybvNR5lv3xYd2wU7Z3c=', '2022-11-08 04:02:42.401069', 1, 'jesus', '', '', 'admin@mail.com', 1, 1, '2022-11-02 14:51:25.809336');

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
(1, '2022-11-05 18:47:59.082684', '1', 'id: 1 | pertenece: id: 5 | titulo: a...', 1, '[{\"added\": {}}]', 9, 1),
(2, '2022-11-05 18:48:17.324980', '2', 'id: 2 | pertenece: id: 5 | titulo: a...', 1, '[{\"added\": {}}]', 9, 1);

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
(7, 'authtoken', 'token'),
(8, 'authtoken', 'tokenproxy'),
(5, 'contenttypes', 'contenttype'),
(16, 'main', 'dialogue'),
(15, 'main', 'option'),
(9, 'main', 'page'),
(14, 'main', 'question'),
(13, 'main', 'repeatphrase'),
(12, 'main', 'story'),
(10, 'main', 'tag'),
(11, 'main', 'user'),
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
(1, 'contenttypes', '0001_initial', '2022-11-02 14:47:35.413050'),
(2, 'auth', '0001_initial', '2022-11-02 14:47:35.931173'),
(3, 'admin', '0001_initial', '2022-11-02 14:47:36.056580'),
(4, 'admin', '0002_logentry_remove_auto_add', '2022-11-02 14:47:36.064720'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2022-11-02 14:47:36.074585'),
(6, 'contenttypes', '0002_remove_content_type_name', '2022-11-02 14:47:36.157114'),
(7, 'auth', '0002_alter_permission_name_max_length', '2022-11-02 14:47:36.346731'),
(8, 'auth', '0003_alter_user_email_max_length', '2022-11-02 14:47:36.371256'),
(9, 'auth', '0004_alter_user_username_opts', '2022-11-02 14:47:36.380897'),
(10, 'auth', '0005_alter_user_last_login_null', '2022-11-02 14:47:36.430057'),
(11, 'auth', '0006_require_contenttypes_0002', '2022-11-02 14:47:36.434435'),
(12, 'auth', '0007_alter_validators_add_error_messages', '2022-11-02 14:47:36.442836'),
(13, 'auth', '0008_alter_user_username_max_length', '2022-11-02 14:47:36.463942'),
(14, 'auth', '0009_alter_user_last_name_max_length', '2022-11-02 14:47:36.480830'),
(15, 'auth', '0010_alter_group_name_max_length', '2022-11-02 14:47:36.501197'),
(16, 'auth', '0011_update_proxy_permissions', '2022-11-02 14:47:36.509194'),
(17, 'auth', '0012_alter_user_first_name_max_length', '2022-11-02 14:47:36.548249'),
(18, 'authtoken', '0001_initial', '2022-11-02 14:47:36.634164'),
(19, 'authtoken', '0002_auto_20160226_1747', '2022-11-02 14:47:36.658021'),
(20, 'authtoken', '0003_tokenproxy', '2022-11-02 14:47:36.662885'),
(21, 'main', '0001_initial', '2022-11-02 14:47:37.259253'),
(22, 'sessions', '0001_initial', '2022-11-02 14:47:37.361951');

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
('asdqdcs5qdn4bstbxzvwxwdie2l6fq5e', '.eJxVjMsOwiAQRf-FtSFQeRSX7vsNZGYYpGogKe3K-O_apAvd3nPOfYkI21ri1nmJcxIXocXpd0OgB9cdpDvUW5PU6rrMKHdFHrTLqSV-Xg_376BAL9_aKM42QHA6ZxxyUNaRZVSJLfpwdqSs1zCqwF6PXmfHiQIa7cn6ZAYU7w_oKTfm:1osFow:SyqrGqotgF0ZEDc5JxcJaQHp2Ux_G2wHTrsPVrx756s', '2022-11-22 04:02:42.407141');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `main_page_dialogue`
--

CREATE TABLE `main_page_dialogue` (
  `id` int(11) NOT NULL,
  `name` varchar(30) NOT NULL,
  `content` varchar(255) NOT NULL,
  `translation` varchar(255) NOT NULL,
  `page_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `main_page_question`
--

CREATE TABLE `main_page_question` (
  `id` int(11) NOT NULL,
  `question` varchar(255) NOT NULL,
  `page_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `main_page_question_option`
--

CREATE TABLE `main_page_question_option` (
  `id` int(11) NOT NULL,
  `answer` varchar(255) NOT NULL,
  `correct` tinyint(1) NOT NULL,
  `question_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `main_page_repeat_phrase`
--

CREATE TABLE `main_page_repeat_phrase` (
  `id` int(11) NOT NULL,
  `content` varchar(255) NOT NULL,
  `translation` varchar(255) NOT NULL,
  `page_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `main_story`
--

CREATE TABLE `main_story` (
  `id` int(11) NOT NULL,
  `title` varchar(100) NOT NULL,
  `cover` varchar(100) NOT NULL,
  `description` varchar(100) DEFAULT NULL,
  `route` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `main_story`
--

INSERT INTO `main_story` (`id`, `title`, `cover`, `description`, `route`) VALUES
(1, 'Una historia de perritos', 'imagenes/portadas/descarga.jpg', NULL, 'una-historia-de-perritos'),
(5, 'a', 'imagenes/portadas/peakpx.jpg', NULL, 'a');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `main_story_page`
--

CREATE TABLE `main_story_page` (
  `id` int(11) NOT NULL,
  `story_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `main_story_page`
--

INSERT INTO `main_story_page` (`id`, `story_id`) VALUES
(1, 5),
(2, 5);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `main_story_tag`
--

CREATE TABLE `main_story_tag` (
  `id` bigint(20) NOT NULL,
  `story_id` int(11) NOT NULL,
  `tag_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `main_story_tag`
--

INSERT INTO `main_story_tag` (`id`, `story_id`, `tag_id`) VALUES
(1, 1, 1),
(2, 1, 2),
(4, 5, 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `main_tag`
--

CREATE TABLE `main_tag` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `main_tag`
--

INSERT INTO `main_tag` (`id`, `name`) VALUES
(1, 'Historia'),
(2, 'Animales'),
(3, 'Programación'),
(4, 'Computación'),
(5, 'Escuela');

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
-- Indices de la tabla `main_page_dialogue`
--
ALTER TABLE `main_page_dialogue`
  ADD PRIMARY KEY (`id`),
  ADD KEY `main_page_dialogue_page_id_8b39dc2b_fk_main_story_page_id` (`page_id`);

--
-- Indices de la tabla `main_page_question`
--
ALTER TABLE `main_page_question`
  ADD PRIMARY KEY (`id`),
  ADD KEY `main_page_question_page_id_6eea5b3a_fk_main_story_page_id` (`page_id`);

--
-- Indices de la tabla `main_page_question_option`
--
ALTER TABLE `main_page_question_option`
  ADD PRIMARY KEY (`id`),
  ADD KEY `main_page_question_o_question_id_dc4dc535_fk_main_page` (`question_id`);

--
-- Indices de la tabla `main_page_repeat_phrase`
--
ALTER TABLE `main_page_repeat_phrase`
  ADD PRIMARY KEY (`id`),
  ADD KEY `main_page_repeat_phrase_page_id_4ff7690b_fk_main_story_page_id` (`page_id`);

--
-- Indices de la tabla `main_story`
--
ALTER TABLE `main_story`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `route` (`route`);

--
-- Indices de la tabla `main_story_page`
--
ALTER TABLE `main_story_page`
  ADD PRIMARY KEY (`id`),
  ADD KEY `main_story_page_story_id_aead7df9_fk_main_story_id` (`story_id`);

--
-- Indices de la tabla `main_story_tag`
--
ALTER TABLE `main_story_tag`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `main_story_tag_story_id_tag_id_e3c7066b_uniq` (`story_id`,`tag_id`),
  ADD KEY `main_story_tag_tag_id_cd367811_fk_main_tag_id` (`tag_id`);

--
-- Indices de la tabla `main_tag`
--
ALTER TABLE `main_tag`
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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=65;

--
-- AUTO_INCREMENT de la tabla `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT de la tabla `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT de la tabla `main_page_dialogue`
--
ALTER TABLE `main_page_dialogue`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `main_page_question`
--
ALTER TABLE `main_page_question`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `main_page_question_option`
--
ALTER TABLE `main_page_question_option`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `main_page_repeat_phrase`
--
ALTER TABLE `main_page_repeat_phrase`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `main_story`
--
ALTER TABLE `main_story`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT de la tabla `main_story_page`
--
ALTER TABLE `main_story_page`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `main_story_tag`
--
ALTER TABLE `main_story_tag`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `main_tag`
--
ALTER TABLE `main_tag`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `main_user`
--
ALTER TABLE `main_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

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

--
-- Filtros para la tabla `main_page_dialogue`
--
ALTER TABLE `main_page_dialogue`
  ADD CONSTRAINT `main_page_dialogue_page_id_8b39dc2b_fk_main_story_page_id` FOREIGN KEY (`page_id`) REFERENCES `main_story_page` (`id`);

--
-- Filtros para la tabla `main_page_question`
--
ALTER TABLE `main_page_question`
  ADD CONSTRAINT `main_page_question_page_id_6eea5b3a_fk_main_story_page_id` FOREIGN KEY (`page_id`) REFERENCES `main_story_page` (`id`);

--
-- Filtros para la tabla `main_page_question_option`
--
ALTER TABLE `main_page_question_option`
  ADD CONSTRAINT `main_page_question_o_question_id_dc4dc535_fk_main_page` FOREIGN KEY (`question_id`) REFERENCES `main_page_question` (`id`);

--
-- Filtros para la tabla `main_page_repeat_phrase`
--
ALTER TABLE `main_page_repeat_phrase`
  ADD CONSTRAINT `main_page_repeat_phrase_page_id_4ff7690b_fk_main_story_page_id` FOREIGN KEY (`page_id`) REFERENCES `main_story_page` (`id`);

--
-- Filtros para la tabla `main_story_page`
--
ALTER TABLE `main_story_page`
  ADD CONSTRAINT `main_story_page_story_id_aead7df9_fk_main_story_id` FOREIGN KEY (`story_id`) REFERENCES `main_story` (`id`);

--
-- Filtros para la tabla `main_story_tag`
--
ALTER TABLE `main_story_tag`
  ADD CONSTRAINT `main_story_tag_story_id_76a647f2_fk_main_story_id` FOREIGN KEY (`story_id`) REFERENCES `main_story` (`id`),
  ADD CONSTRAINT `main_story_tag_tag_id_cd367811_fk_main_tag_id` FOREIGN KEY (`tag_id`) REFERENCES `main_tag` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
