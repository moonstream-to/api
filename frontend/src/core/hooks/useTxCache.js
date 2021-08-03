class TxCashe {
    currentTransaction = undefined
    getCurrentTransaction(){return this.currentTransaction}
    setCurrentTransaction(transaction){ this.currentTransaction = transaction}
}
const useTxCashe = new TxCashe();
export default useTxCashe;