// import { useState, useEffect } from "react";
import { useQuery } from "react-query";
import { useToast } from ".";
import { queryCacheProps } from "./hookCommon";
import { NFTService } from "../services";

const useNFTs = (query) => {
  const toast = useToast();

  const getNFTStats = async (query) => {
    const response = await NFTService.getNFTStats(query);
    return response.data.data;
  };

  const nftCache = useQuery(["NFTs", query], getNFTStats, {
    ...queryCacheProps,
    onError: (error) => {
      toast(error, "error");
    },
  });
  return {
    nftCache,
  };
};

export default useNFTs;
