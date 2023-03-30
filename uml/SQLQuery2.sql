-- SQLINES LICENSE FOR EVALUATION USE ONLY
CREATE TABLE tutor (
  Id int NOT NULL IDENTITY,
  Name varchar(255) NOT NULL,
  CreationDate datetime2(0) DEFAULT GETDATE(),
  PRIMARY KEY (Id)
)  ;

-- SQLINES LICENSE FOR EVALUATION USE ONLY
CREATE TABLE semester (
  Id int NOT NULL IDENTITY,
  SemesterName varchar(255) NOT NULL,
  SemesterYear int DEFAULT NULL,
  Inprogress smallint DEFAULT NULL,
  CreationDate datetime2(0) DEFAULT GETDATE(),
  PRIMARY KEY (Id)
)  ;

-- SQLINES LICENSE FOR EVALUATION USE ONLY
CREATE TABLE students (
  Id int NOT NULL IDENTITY,
  Name varchar(255) NOT NULL,
  Gender varchar(45) DEFAULT NULL,
  Email varchar(45) DEFAULT NULL,
  Phone varchar(45) DEFAULT NULL,
  CreationDate datetime2(0) DEFAULT GETDATE(),
  PRIMARY KEY (Id)
)  ;


-- SQLINES LICENSE FOR EVALUATION USE ONLY
CREATE TABLE modules (
  Id int NOT NULL IDENTITY,
  ModuleName varchar(255) NOT NULL,
  TutorId int DEFAULT NULL,
  SemesterId int NOT NULL,
  CreationDate datetime2(0) DEFAULT GETDATE(),
  PRIMARY KEY (Id)
,
  CONSTRAINT module_fk_sem FOREIGN KEY (SemesterId) REFERENCES semester (Id),
  CONSTRAINT module_fk_tutor FOREIGN KEY (TutorId) REFERENCES tutor (Id)
)  ;

CREATE INDEX modules_sem_idx ON modules (SemesterId);
CREATE INDEX module_fk_tutor ON modules (TutorId);



-- SQLINES LICENSE FOR EVALUATION USE ONLY
CREATE TABLE studentattendance (
  Id int NOT NULL IDENTITY,
  StudentId int DEFAULT NULL,
  ModuleId int DEFAULT NULL,
  IsCheckedIn smallint DEFAULT NULL,
  CreationDate datetime2(0) DEFAULT GETDATE(),
  PRIMARY KEY (Id)
,
  CONSTRAINT studentattendance_ibfk_1 FOREIGN KEY (StudentId) REFERENCES students (Id),
  CONSTRAINT studentattendance_ibfk_2 FOREIGN KEY (ModuleId) REFERENCES modules (Id)
)  ;

CREATE INDEX StudentId ON studentattendance (StudentId);
CREATE INDEX ModuleId ON studentattendance (ModuleId);


-- SQLINES LICENSE FOR EVALUATION USE ONLY
CREATE TABLE studentcheck (
  Id int NOT NULL IDENTITY,
  StudentId int DEFAULT NULL,
  ModuleId int DEFAULT NULL,
  CreationDate datetime2(0) DEFAULT GETDATE(),
  PRIMARY KEY (Id)
,
  CONSTRAINT studentcheck_ibfk_1 FOREIGN KEY (StudentId) REFERENCES students (Id),
  CONSTRAINT studentcheck_ibfk_2 FOREIGN KEY (ModuleId) REFERENCES modules (Id)
) ;

CREATE INDEX StudentId ON studentcheck (StudentId);
CREATE INDEX ModuleId ON studentcheck (ModuleId);




