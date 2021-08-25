import logging
from typing import Dict, Optional

from sqlalchemy.sql.expression import true

from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from moonstreamdb.db import yield_db_session
from moonstreamdb.models import EthereumAddress
from sqlalchemy.orm import Session
