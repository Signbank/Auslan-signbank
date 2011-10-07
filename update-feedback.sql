BEGIN;

ALTER TABLE "feedback_generalfeedback" ADD 
    "status" varchar(10) NOT NULL DEFAULT "unread"
;
ALTER TABLE "feedback_signfeedback" ADD 
    "status" varchar(10) NOT NULL DEFAULT "unread"
;
ALTER TABLE "feedback_missingsignfeedback" ADD 
    "status" varchar(10) NOT NULL DEFAULT "unread"
;
COMMIT;
