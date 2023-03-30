USE [master]
GO
/****** Object:  Database [uninorthwest]    Script Date: 3/18/2023 11:35:47 AM ******/
CREATE DATABASE [uninorthwest]
 CONTAINMENT = NONE
 ON  PRIMARY 
( NAME = N'uninorthwest', FILENAME = N'C:\Program Files\Microsoft SQL Server\MSSQL15.MSSQLSERVER\MSSQL\DATA\uninorthwest.mdf' , SIZE = 8192KB , MAXSIZE = UNLIMITED, FILEGROWTH = 65536KB )
 LOG ON 
( NAME = N'uninorthwest_log', FILENAME = N'C:\Program Files\Microsoft SQL Server\MSSQL15.MSSQLSERVER\MSSQL\DATA\uninorthwest_log.ldf' , SIZE = 8192KB , MAXSIZE = 2048GB , FILEGROWTH = 65536KB )
 WITH CATALOG_COLLATION = DATABASE_DEFAULT
GO
ALTER DATABASE [uninorthwest] SET COMPATIBILITY_LEVEL = 150
GO
IF (1 = FULLTEXTSERVICEPROPERTY('IsFullTextInstalled'))
begin
EXEC [uninorthwest].[dbo].[sp_fulltext_database] @action = 'enable'
end
GO
ALTER DATABASE [uninorthwest] SET ANSI_NULL_DEFAULT OFF 
GO
ALTER DATABASE [uninorthwest] SET ANSI_NULLS OFF 
GO
ALTER DATABASE [uninorthwest] SET ANSI_PADDING OFF 
GO
ALTER DATABASE [uninorthwest] SET ANSI_WARNINGS OFF 
GO
ALTER DATABASE [uninorthwest] SET ARITHABORT OFF 
GO
ALTER DATABASE [uninorthwest] SET AUTO_CLOSE OFF 
GO
ALTER DATABASE [uninorthwest] SET AUTO_SHRINK OFF 
GO
ALTER DATABASE [uninorthwest] SET AUTO_UPDATE_STATISTICS ON 
GO
ALTER DATABASE [uninorthwest] SET CURSOR_CLOSE_ON_COMMIT OFF 
GO
ALTER DATABASE [uninorthwest] SET CURSOR_DEFAULT  GLOBAL 
GO
ALTER DATABASE [uninorthwest] SET CONCAT_NULL_YIELDS_NULL OFF 
GO
ALTER DATABASE [uninorthwest] SET NUMERIC_ROUNDABORT OFF 
GO
ALTER DATABASE [uninorthwest] SET QUOTED_IDENTIFIER OFF 
GO
ALTER DATABASE [uninorthwest] SET RECURSIVE_TRIGGERS OFF 
GO
ALTER DATABASE [uninorthwest] SET  DISABLE_BROKER 
GO
ALTER DATABASE [uninorthwest] SET AUTO_UPDATE_STATISTICS_ASYNC OFF 
GO
ALTER DATABASE [uninorthwest] SET DATE_CORRELATION_OPTIMIZATION OFF 
GO
ALTER DATABASE [uninorthwest] SET TRUSTWORTHY OFF 
GO
ALTER DATABASE [uninorthwest] SET ALLOW_SNAPSHOT_ISOLATION OFF 
GO
ALTER DATABASE [uninorthwest] SET PARAMETERIZATION SIMPLE 
GO
ALTER DATABASE [uninorthwest] SET READ_COMMITTED_SNAPSHOT OFF 
GO
ALTER DATABASE [uninorthwest] SET HONOR_BROKER_PRIORITY OFF 
GO
ALTER DATABASE [uninorthwest] SET RECOVERY FULL 
GO
ALTER DATABASE [uninorthwest] SET  MULTI_USER 
GO
ALTER DATABASE [uninorthwest] SET PAGE_VERIFY CHECKSUM  
GO
ALTER DATABASE [uninorthwest] SET DB_CHAINING OFF 
GO
ALTER DATABASE [uninorthwest] SET FILESTREAM( NON_TRANSACTED_ACCESS = OFF ) 
GO
ALTER DATABASE [uninorthwest] SET TARGET_RECOVERY_TIME = 60 SECONDS 
GO
ALTER DATABASE [uninorthwest] SET DELAYED_DURABILITY = DISABLED 
GO
ALTER DATABASE [uninorthwest] SET ACCELERATED_DATABASE_RECOVERY = OFF  
GO
EXEC sys.sp_db_vardecimal_storage_format N'uninorthwest', N'ON'
GO
ALTER DATABASE [uninorthwest] SET QUERY_STORE = OFF
GO
USE [uninorthwest]
GO
/****** Object:  Table [dbo].[modules]    Script Date: 3/18/2023 11:35:47 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[modules](
	[Id] [int] IDENTITY(1,1) NOT NULL,
	[ModuleName] [varchar](255) NOT NULL,
	[TutorId] [int] NULL,
	[SemesterId] [int] NOT NULL,
	[CreationDate] [datetime2](0) NULL,
PRIMARY KEY CLUSTERED 
(
	[Id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[semester]    Script Date: 3/18/2023 11:35:47 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[semester](
	[Id] [int] IDENTITY(1,1) NOT NULL,
	[SemesterName] [varchar](255) NOT NULL,
	[SemesterYear] [int] NULL,
	[Inprogress] [smallint] NULL,
	[CreationDate] [datetime2](0) NULL,
PRIMARY KEY CLUSTERED 
(
	[Id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[studentattendance]    Script Date: 3/18/2023 11:35:47 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[studentattendance](
	[Id] [int] IDENTITY(1,1) NOT NULL,
	[StudentId] [int] NULL,
	[ModuleId] [int] NULL,
	[IsCheckedIn] [smallint] NULL,
	[CreationDate] [datetime2](0) NULL,
PRIMARY KEY CLUSTERED 
(
	[Id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[studentcheck]    Script Date: 3/18/2023 11:35:47 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[studentcheck](
	[Id] [int] IDENTITY(1,1) NOT NULL,
	[StudentId] [int] NULL,
	[ModuleId] [int] NULL,
	[CreationDate] [datetime2](0) NULL,
PRIMARY KEY CLUSTERED 
(
	[Id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[students]    Script Date: 3/18/2023 11:35:47 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[students](
	[Id] [int] IDENTITY(1,1) NOT NULL,
	[Name] [varchar](255) NOT NULL,
	[Gender] [varchar](45) NULL,
	[Email] [varchar](45) NULL,
	[Phone] [varchar](45) NULL,
	[CreationDate] [datetime2](0) NULL,
PRIMARY KEY CLUSTERED 
(
	[Id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[tutor]    Script Date: 3/18/2023 11:35:47 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[tutor](
	[Id] [int] IDENTITY(1,1) NOT NULL,
	[Name] [varchar](255) NOT NULL,
	[CreationDate] [datetime2](0) NULL,
PRIMARY KEY CLUSTERED 
(
	[Id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Index [module_fk_tutor]    Script Date: 3/18/2023 11:35:47 AM ******/
CREATE NONCLUSTERED INDEX [module_fk_tutor] ON [dbo].[modules]
(
	[TutorId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
/****** Object:  Index [modules_sem_idx]    Script Date: 3/18/2023 11:35:47 AM ******/
CREATE NONCLUSTERED INDEX [modules_sem_idx] ON [dbo].[modules]
(
	[SemesterId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
/****** Object:  Index [ModuleId]    Script Date: 3/18/2023 11:35:47 AM ******/
CREATE NONCLUSTERED INDEX [ModuleId] ON [dbo].[studentattendance]
(
	[ModuleId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
/****** Object:  Index [StudentId]    Script Date: 3/18/2023 11:35:47 AM ******/
CREATE NONCLUSTERED INDEX [StudentId] ON [dbo].[studentattendance]
(
	[StudentId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
/****** Object:  Index [ModuleId]    Script Date: 3/18/2023 11:35:47 AM ******/
CREATE NONCLUSTERED INDEX [ModuleId] ON [dbo].[studentcheck]
(
	[ModuleId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
/****** Object:  Index [StudentId]    Script Date: 3/18/2023 11:35:47 AM ******/
CREATE NONCLUSTERED INDEX [StudentId] ON [dbo].[studentcheck]
(
	[StudentId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
ALTER TABLE [dbo].[modules] ADD  DEFAULT (NULL) FOR [TutorId]
GO
ALTER TABLE [dbo].[modules] ADD  DEFAULT (getdate()) FOR [CreationDate]
GO
ALTER TABLE [dbo].[semester] ADD  DEFAULT (NULL) FOR [SemesterYear]
GO
ALTER TABLE [dbo].[semester] ADD  DEFAULT (NULL) FOR [Inprogress]
GO
ALTER TABLE [dbo].[semester] ADD  DEFAULT (getdate()) FOR [CreationDate]
GO
ALTER TABLE [dbo].[studentattendance] ADD  DEFAULT (NULL) FOR [StudentId]
GO
ALTER TABLE [dbo].[studentattendance] ADD  DEFAULT (NULL) FOR [ModuleId]
GO
ALTER TABLE [dbo].[studentattendance] ADD  DEFAULT (NULL) FOR [IsCheckedIn]
GO
ALTER TABLE [dbo].[studentattendance] ADD  DEFAULT (getdate()) FOR [CreationDate]
GO
ALTER TABLE [dbo].[studentcheck] ADD  DEFAULT (NULL) FOR [StudentId]
GO
ALTER TABLE [dbo].[studentcheck] ADD  DEFAULT (NULL) FOR [ModuleId]
GO
ALTER TABLE [dbo].[studentcheck] ADD  DEFAULT (getdate()) FOR [CreationDate]
GO
ALTER TABLE [dbo].[students] ADD  DEFAULT (NULL) FOR [Gender]
GO
ALTER TABLE [dbo].[students] ADD  DEFAULT (NULL) FOR [Email]
GO
ALTER TABLE [dbo].[students] ADD  DEFAULT (NULL) FOR [Phone]
GO
ALTER TABLE [dbo].[students] ADD  DEFAULT (getdate()) FOR [CreationDate]
GO
ALTER TABLE [dbo].[tutor] ADD  DEFAULT (getdate()) FOR [CreationDate]
GO
ALTER TABLE [dbo].[modules]  WITH CHECK ADD  CONSTRAINT [module_fk_sem] FOREIGN KEY([SemesterId])
REFERENCES [dbo].[semester] ([Id])
GO
ALTER TABLE [dbo].[modules] CHECK CONSTRAINT [module_fk_sem]
GO
ALTER TABLE [dbo].[modules]  WITH CHECK ADD  CONSTRAINT [module_fk_tutor] FOREIGN KEY([TutorId])
REFERENCES [dbo].[tutor] ([Id])
GO
ALTER TABLE [dbo].[modules] CHECK CONSTRAINT [module_fk_tutor]
GO
ALTER TABLE [dbo].[studentattendance]  WITH CHECK ADD  CONSTRAINT [studentattendance_ibfk_1] FOREIGN KEY([StudentId])
REFERENCES [dbo].[students] ([Id])
GO
ALTER TABLE [dbo].[studentattendance] CHECK CONSTRAINT [studentattendance_ibfk_1]
GO
ALTER TABLE [dbo].[studentattendance]  WITH CHECK ADD  CONSTRAINT [studentattendance_ibfk_2] FOREIGN KEY([ModuleId])
REFERENCES [dbo].[modules] ([Id])
GO
ALTER TABLE [dbo].[studentattendance] CHECK CONSTRAINT [studentattendance_ibfk_2]
GO
ALTER TABLE [dbo].[studentcheck]  WITH CHECK ADD  CONSTRAINT [studentcheck_ibfk_1] FOREIGN KEY([StudentId])
REFERENCES [dbo].[students] ([Id])
GO
ALTER TABLE [dbo].[studentcheck] CHECK CONSTRAINT [studentcheck_ibfk_1]
GO
ALTER TABLE [dbo].[studentcheck]  WITH CHECK ADD  CONSTRAINT [studentcheck_ibfk_2] FOREIGN KEY([ModuleId])
REFERENCES [dbo].[modules] ([Id])
GO
ALTER TABLE [dbo].[studentcheck] CHECK CONSTRAINT [studentcheck_ibfk_2]
GO
USE [master]
GO
ALTER DATABASE [uninorthwest] SET  READ_WRITE 
GO
